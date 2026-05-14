#executar pip install streamlit requests pdfplumber
#para executar o streamlit digit streamlit run app.py no terminal

### Para consertar:
# O site faz o PDF ser obrigatório ser obri8gatório, o certo seria ser opcional.

import streamlit as st
import requests
import pdfplumber
from datetime import datetime

# Configurações da Página
st.set_page_config(page_title="AI Job Hunter", page_icon="🤖")

st.title("🤖 Agente de Gestão de Vagas")
st.markdown("Envie o link da vaga e seu currículo para análise de Match e salvamento automático.")

# URL do seu Webhook do Make.com (Substitua após criar no Make)
MAKE_WEBHOOK_URL = "https://hook.us1.make.com/seu_codigo_aqui"

with st.form("job_form"):
    job_link = st.text_input("Link da Vaga:", placeholder="https://linkedin.com/jobs/...")
    uploaded_file = st.file_uploader("Upload do seu Currículo (PDF)", type="pdf")
    
    submit_button = st.form_submit_button("Analisar e Salvar")

if submit_button:
    if job_link and uploaded_file:
        with st.spinner("Processando currículo e enviando dados..."):
            try:
                # 1. Extração de texto do PDF
                with pdfplumber.open(uploaded_file) as pdf:
                    resume_text = ""
                    for page in pdf.pages:
                        resume_text += page.extract_text()

                # 2. Preparação dos dados para o Make.com
                payload = {
                    "source": "streamlit",
                    "link_vaga": job_link,
                    "curriculo_raw": resume_text,
                    "timestamp": datetime.now().isoformat()
                }

                # 3. Envio para o Webhook
                response = requests.post("https://hook.eu1.make.com/mn8z6u3dyqgavjquk5er4mlit89wl1ta", json=payload)

                if response.status_code == 200:
                    st.success("✅ Dados enviados com sucesso! Verifique seu Notion e Telegram.")
                else:
                    st.error(f"Erro no servidor: {response.status_code}")

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, preencha o link e faça o upload do PDF.")