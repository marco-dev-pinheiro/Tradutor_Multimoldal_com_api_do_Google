import streamlit as st
import os
from cerebro_tradutor import pipeline_processamento
import base64

# Configuração da página
st.set_page_config(page_title="Tradutor IA", page_icon="🎙️")

st.title("🎙️ Tradutor Inteligente Mp621 Com IA integrada ")
st.write("Grave seu áudio em um idioma e receba a tradução e voz em tempo real.")

audio_value = st.audio_input("Clique para gravar")

if audio_value:
    audio_bytes = audio_value.read()
    audio_base64 = f"data:audio/wav;base64,{base64.b64encode(audio_bytes).decode()}"

    with st.spinner("Processando tradução..."):
        orig, trad, path = pipeline_processamento(audio_base64)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original")
            st.info(orig)
        with col2:
            st.subheader("Tradução")
            st.success(trad)

        if path:
            st.audio(path, format="audio/mp3", autoplay=True)
            st.caption("✅ Tradução concluída com sucesso!")

