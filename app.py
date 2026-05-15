# python -m streamlit run app.py



import streamlit as st

import requests

import pdfplumber

from datetime import datetime



# Configurações da Página

st.set_page_config(page_title="AI Job Hunter", page_icon="🤖", layout="centered")



# URLs dos Webhooks do Make.com (Insira as URLs corretas geradas pelo Make aqui)

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/mn8z6u3dyqgavjquk5er4mlit89wl1ta"

MAKE_WEBHOOK_BUSCA_URL = "https://hook.eu1.make.com/edd7mejxpt2pku4y435hpm28l71awgsl"



st.title("🤖 Agente de Gestão de Vagas")



# --- SEÇÃO 1: FORMULÁRIO DE ANÁLISE ---

st.markdown("### 📝 Analisador de Match")

st.info("Envie o link da vaga e seu currículo para análise de Match e salvamento automático.")



with st.form("job_form"):

  job_link = st.text_input("Link da Vaga:", placeholder="https://linkedin.com/jobs/...")

  uploaded_file = st.file_uploader("Upload do seu Currículo (Opcional)", type="pdf")

  

  submit_button = st.form_submit_button("Analisar e Salvar")



if submit_button:

  # O validador exige apenas o link da vaga

  if job_link:

    with st.spinner("Processando e enviando dados..."):

      try:

        # 1. Tratamento do Currículo (Opcional)

        resume_text = "Nenhum currículo enviado."

        

        if uploaded_file is not None:

          with pdfplumber.open(uploaded_file) as pdf:

            content = []

            for page in pdf.pages:

              text = page.extract_text()

              if text:

                content.append(text)

            

            if content:

              resume_text = "\n".join(content)



        # 2. Preparação do Payload

        payload = {

          "source": "streamlit_analysis",

          "link_vaga": job_link,

          "curriculo_raw": resume_text,

          "timestamp": datetime.now().isoformat()

        }



        # 3. Envio para o Webhook de Análise

        response = requests.post(MAKE_WEBHOOK_URL, json=payload)



        if response.status_code == 200:

          st.success("✅ Dados enviados com sucesso! Verifique seu Notion e Telegram.")

        else:

          st.error(f"Erro no servidor: {response.status_code}")



      except Exception as e:

        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

  else:

    st.warning("O campo 'Link da Vaga' é obrigatório para prosseguir.")



st.divider() # Linha visual para separar as seções



# --- SEÇÃO 2: BUSCADOR INTELIGENTE ---

st.markdown("### 🔍 Buscador de Vagas Inteligente")

st.write("Diga ao agente que tipo de vaga você procura e ele fará uma varredura na web.")



# Campo de busca com valor padrão

search_query = st.text_input(

  "O que deseja buscar?",

  value="Buscar 3 vagas de Dev Júnior em Mogi das Cruzes ou Próximo"

)



if st.button("Buscar Vagas na Web"):

  if search_query:

    with st.spinner("O Agente está vasculhando a internet por vagas recentes..."):

      try:

        # Preparação do Payload de Busca (corrigido para usar search_query)

        payload_busca = {

          "source": "streamlit_search",

          "termo_busca": search_query,

          "timestamp": datetime.now().isoformat()

        }

        

        # Envio para o Webhook de Busca

        resp_busca = requests.post(MAKE_WEBHOOK_BUSCA_URL, json=payload_busca)

        

        if resp_busca.status_code == 200:

          st.success("🔍 Varredura concluída com sucesso!")

          st.subheader("💼 Vagas Encontradas pelo Agente:")

          

          # Exibe o Markdown gerado pelo Gemini que o Webhook Response enviou de volta

          st.markdown(resp_busca.text)

        else:

          st.error(f"Erro ao acionar busca: {resp_busca.status_code}")

          

      except Exception as e:

        st.error(f"Falha na conexão com o buscador: {e}")

  else:

    st.warning("Por favor, digite um termo de busca.")