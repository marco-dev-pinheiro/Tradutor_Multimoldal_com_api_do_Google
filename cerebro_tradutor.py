import os
import base64
import whisper
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gtts import gTTS

# 1. Carregamento da Chave (Prioridade para st.secrets)
load_dotenv()
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Chave de API não configurada nas Secrets do Streamlit!")
    st.stop()

# 2. Inicialização dos Clientes
client = genai.Client(api_key=api_key)

# 3. Cache do Modelo Whisper (Evita carregar toda vez que clicar no botão)
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

model_whisper = load_whisper()


def pipeline_processamento(audio_base64):
    try:
        # 1. Decodificação do Áudio
        dados_audio = base64.b64decode(audio_base64.split(",")[1])
        arquivo_entrada = "entrada.wav"
        with open(arquivo_entrada, "wb") as f:
            f.write(dados_audio)

        # 2. Transcrição (Whisper)
        resultado_transcricao = model_whisper.transcribe(arquivo_entrada, fp16=False, task="transcribe")
        texto_original = resultado_transcricao["text"].strip()

       # 3. Tradução com Lógica de Inversão (Gemini)
        instrucao_sistema = """Você é um tradutor automático rigoroso.
        Sua saída deve seguir EXATAMENTE o formato: codigo|texto

        Regras de detecção:
        - Se o usuário falar em Português -> Retorne: en|tradução para inglês
        - Se o usuário falar em Inglês -> Retorne: pt|tradução para português

        Exemplos de saída esperada:
        en|Good morning, how can I help you?
        pt|Bom dia, como posso ajudar?

        NUNCA adicione explicações, aspas ou textos extras. Apenas 'codigo|texto'."""
        try:
            resposta = client.models.generate_content(
                model='gemini-2.0-flash', # Versão atual estável
                contents=f"Traduza: {texto_original}",
                config=types.GenerateContentConfig(
                    system_instruction=instrucao_sistema,
                    temperature=0.1
                )
            )
            saida_bruta = resposta.text.strip()
        except Exception as erro_api:
            if "429" in str(erro_api):
                return texto_original, "Erro: Limite atingido. Aguarde 1 min.", None
            raise erro_api

        # 4. Parsing e Síntese de Voz (gTTS)
        if "|" in saida_bruta:
            codigo_idioma, texto_traduzido = [s.strip() for s in saida_bruta.split("|", 1)]
            idioma_voz = "pt" if "pt" in codigo_idioma.lower() else "en"
        else:
            texto_traduzido = saida_bruta
            idioma_voz = "pt"

        arquivo_saida = "saida.mp3"
        sintetizador = gTTS(text=texto_traduzido, lang=idioma_voz)
        sintetizador.save(arquivo_saida)

        return texto_original, texto_traduzido, arquivo_saida

    except Exception as erro:
        return f"Erro: {str(erro)}", "Falha no processamento", None