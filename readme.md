# 🎙️ Tradutor Inteligente Multi-Modal (Gemini 2.0 + Whisper)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75C2?style=for-the-badge&logo=googlegemini&logoColor=white)
![OpenAI Whisper](https://img.shields.io/badge/OpenAI%20Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)

🎙️ Multimodal AI Translation Pipeline (Gemini 2.0 & Whisper)
Este repositório contém uma aplicação de tradução simultânea baseada em uma pipeline assíncrona de processamento de linguagem natural (NLP). O sistema integra modelos de Speech-to-Text (STT), Large Language Models (LLM) e Text-to-Speech (TTS) em um fluxo de dados desacoplado.

🏗️ Arquitetura do Sistema
O projeto foi construído seguindo o padrão de Separação de Preocupações (SoC), dividindo a inteligência de processamento da camada de apresentação.

🔬 Fluxo de Processamento de Dados (Pipeline)
Ingestão e Pré-processamento de Áudio:

O sinal de áudio é capturado via MediaRecorder API (Frontend) e transmitido via buffer Base64.

Normalização: O backend decodifica o stream e realiza o re-sampling para 16kHz, formato ideal para o processamento do Encoder do Whisper.

Speech-to-Text (STT) com OpenAI Whisper:

Utilização do modelo base que opera sobre uma arquitetura de Transformer-based sequence-to-sequence.

O áudio é convertido em Log-Mel Spectrograms, processados por um encoder convolucional para extração de features acústicas.

LLM Reasoning & Contextual Translation (Gemini 2.0 Flash):

Implementação de System Instructions rigorosas para garantir uma saída determinística.

Técnica: Zero-shot translation com inferência de código de idioma (ISO 639-1).

Parsing Algorítmico: O retorno do modelo é tratado como uma string estruturada lang_code|content, submetida a um parser que isola os metadados para a próxima etapa.

Neural Speech Synthesis (TTS):

O motor gTTS realiza a síntese baseada no código de idioma extraído dinamicamente no passo anterior.

O resultado é um objeto de áudio serializado, entregue ao cliente via buffer de memória para reprodução imediata.

🛠️ Especificações Técnicas
Gestão de Dependências e Segurança
Environment Isolation: Implementação de .env para gestão de secrets (API Keys), seguindo diretrizes de segurança OWASP.

Dependency Management: Uso de requirements.txt para reprodutibilidade do ambiente e packages.txt para dependências binárias (FFmpeg).

Estrutura de Diretórios
Plaintext
├── src/
│   ├── app.py           # Controller & Streamlit Interface
│   └── cerebro.py       # Engine de Processamento (Logic Layer)
├── notebooks/           # Research & Development (Google Colab)
├── requirements.txt     # Python Dependencies
└── packages.txt         # OS Level Dependencies (FFmpeg)
🚀 Desafios Superados (Edge Cases)
Tratamento de Rate Limiting (Error 429): Implementação de blocos try-except específicos para gerenciar limites de cota da API do Google, garantindo a resiliência do sistema sem interrupção abrupta da execução.

Latência Perceptiva: Otimização do fluxo de áudio para reduzir o Time to First Byte (TTFB) na síntese de voz, utilizando modelos "Flash" para menor tempo de inferência.

👤 Autor
Marco Pinheiro - [LinkedIn](https://www.linkedin.com/in/marco-pinheiro-34256b373/)

Link para o App Streamlit Live
   https://tradutormultimoldal.streamlit.app/
   git clone [https://https://github.com/marco-dev-pinheiro/Tradutor_Multimoldal_com_api_do_Google.git](https://https://github.com/marco-dev-pinheiro/Tradutor_Multimoldal_com_api_do_Google.git)
