import streamlit as st
import requests
import pdfplumber
from datetime import datetime

# Configurações da Página
st.set_page_config(page_title="AI Job Hunter Pro", page_icon="🤖", layout="centered")

# --- CONFIGURAÇÃO DE APENAS 2 WEBHOOKS ---
# Webhook 1: Cuida de todo o fluxo de análise e salvamento (Preview -> Confirmar -> Notion)
MAKE_WEBHOOK_ANALISE_URL = "https://hook.eu1.make.com/mn8z6u3dyqgavjquk5er4mlit89wl1ta"

# Webhook 2: Cuida exclusivamente do buscador inteligente de vagas
MAKE_WEBHOOK_BUSCA_URL = "https://hook.eu1.make.com/edd7mejxpt2pku4y435hpm28l71awgsl"


# --- INICIALIZAÇÃO DO ESTADO (SESSION STATE) ---
if "preview_data" not in st.session_state:
    st.session_state.preview_data = None
if "vaga_enviada" not in st.session_state:
    st.session_state.vaga_enviada = False
if "tem_curriculo" not in st.session_state:
    st.session_state.tem_curriculo = False

st.title("🤖 Agente de Gestão de Vagas")

# --- SEÇÃO 1: ANALISADOR DE MATCH (FLUXO EM 2 ETAPAS) ---
st.markdown("### 📝 Analisador de Match")
st.info("Insira os dados para gerar uma pré-visualização da análise de IA antes de salvar no Notion.")

# Form de Entrada de Dados (Etapa 1)
with st.form("job_input_form"):
    job_link = st.text_input("Link da Vaga:", placeholder="https://linkedin.com/jobs/...")
    uploaded_file = st.file_uploader("Upload do seu Currículo (Opcional)", type="pdf")
    
    generate_preview = st.form_submit_button("Gerar Pré-visualização")

if generate_preview:
    if job_link:
        with st.spinner("O Gemini está analisando a vaga e seu currículo..."):
            try:
                resume_text = "Nenhum currículo enviado."
                has_pdf = False
                
                if uploaded_file is not None: 
                    has_pdf = True
                    with pdfplumber.open(uploaded_file) as pdf:
                        content = [page.extract_text() for page in pdf.pages if page.extract_text()]
                        if content:
                            resume_text = "\n".join(content)

                # Trava de Segurança Front-End / Payload: Guardando o estado real do PDF
                st.session_state.tem_curriculo = has_pdf

                # Enviamos "streamlit_preview" para o Make saber que deve apenas analisar e retornar
                payload_preview = {
                    "source": "streamlit_preview",
                    "link_vaga": job_link,
                    "curriculo_raw": resume_text,
                    "tem_curriculo": has_pdf,
                    "timestamp": datetime.now().isoformat()
                }

                # Chamada síncrona aguardando o Webhook Response do Make
                response = requests.post(MAKE_WEBHOOK_ANALISE_URL, json=payload_preview)

                if response.status_code == 200:
                    # Salva o retorno estruturado no estado da aplicação
                    try:
                         st.session_state.preview_data = response.json()
                         st.session_state.vaga_enviada = False
                         st.rerun()
                    except Exception:
                        st.error(f"Make retornou resposta inválida: {response.text[:300]}")
                else: 
                     st.error(f"Erro na análise do Make/Gemini: {response.status_code}")

            except Exception as e:
                st.error(f"Erro interno no processamento: {e}")
    else:
        st.warning("O link da vaga é obrigatório para gerar o preview.")

# --- MÓDULO DE EXIBIÇÃO E CONFIRMAÇÃO (Etapa 2) ---
if st.session_state.preview_data:
    data = st.session_state.preview_data
    
    st.markdown("---")
    st.markdown("### 📋 Dados Extraídos pela IA")
    st.write("Revise os dados abaixo. Se estiver tudo correto, clique em **Enviar para a Planilha**.")

    # Estilos CSS customizados para os cards com quebra automática de linha (UI/UX Refatorada)
    st.markdown("""
        <style>
            .custom-card-container {
                display: flex;
                flex-direction: column;
                background-color: rgba(151, 166, 195, 0.1);
                border: 1px solid rgba(151, 166, 195, 0.2);
                border-radius: 0.5rem;
                padding: 1rem;
                margin-bottom: 1rem;
                min-height: 105px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            .custom-card-label {
                font-size: 0.85rem;
                color: rgb(151, 166, 195);
                margin-bottom: 0.35rem;
                font-weight: 500;
            }
            .custom-card-value {
                font-size: 1.15rem;
                font-weight: 600;
                color: inherit;
                line-height: 1.4;
                white-space: normal;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
        </style>
    """, unsafe_allow_html=True)

    # Lógica de processamento do Match Score com a Trava Anti-Alucinação
    if st.session_state.tem_curriculo:
        score = data.get("match_score")
        if score is not None and str(score) != "N/A" and score != 0:
            match_value = f"🎯 {score}/10"
        else:
            match_value = "🎯 Sem Score"
    else:
        match_value = "📝 Sem Currículo"

    # Grid Visual utilizando colunas nativas do Streamlit contendo os componentes HTML/CSS customizados
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="custom-card-container">
                <div class="custom-card-label">🏢 Empresa</div>
                <div class="custom-card-value">{data.get("empresa", "Não identificado")}</div>
            </div>
            <div class="custom-card-container">
                <div class="custom-card-label">📍 Cidade</div>
                <div class="custom-card-value">{data.get("cidade", "Não identificado")}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="custom-card-container">
                <div class="custom-card-label">💼 Cargo</div>
                <div class="custom-card-value">{data.get("vaga", "Não identificado")}</div>
            </div>
            <div class="custom-card-container">
                <div class="custom-card-label">💰 Salário Estimado</div>
                <div class="custom-card-value">{data.get("salario", "Não informado")}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class="custom-card-container" style="min-height: 226px; justify-content: center; text-align: center;">
                <div class="custom-card-label">🎯 Match Score</div>
                <div class="custom-card-value" style="font-size: 1.5rem; margin-top: 0.5rem;">{match_value}</div>
            </div>
        """, unsafe_allow_html=True)

    # Links e Datas abaixo das métricas
    st.markdown(f"**📅 Data da Análise:** {data.get('data', datetime.now().strftime('%d/%m/%Y'))}")
    st.markdown(f"**🔗 Link da Vaga:** [{job_link if 'job_link' in locals() else 'Acessar Link'}]({data.get('link_vaga', '#')})")

    # Box de Análise de Currículo Exclusivo (Condicional com trava de segurança anti-alucinação)
    if st.session_state.tem_curriculo:
        feedback_ia = data.get("feedback_ia")
        if feedback_ia and feedback_ia != "Nenhum currículo enviado.":
            with st.chat_message("assistant"):
                st.markdown(f"**Análise de Fit Cultural e Técnico:**\n\n{feedback_ia}")

    # Botão de Confirmação Final (Protegido por um Form para isolar o disparo do webhook)
    if not st.session_state.vaga_enviada:
        with st.form("confirm_save_form"):
            submit_save = st.form_submit_button("🚀 Enviar para a Planilha", type="primary", use_container_width=True)
            
        if submit_save:
            with st.spinner("Salvando no Notion..."):
                try:
                    # Aplicação estrita da trava contra alucinação no Payload Final
                    final_match_score = data.get("match_score", 0) if st.session_state.tem_curriculo else "Sem Currículo"

                    # Prepara o payload de salvamento final enviando estritamente "streamlit_confirmado"
                    payload_save = {
                        "source": "streamlit_confirmado",
                        "vaga": data.get("vaga"),
                        "empresa": data.get("empresa"),
                        "cidade": data.get("cidade"),
                        "salario": data.get("salario"),
                        "match_score": final_match_score,
                        "link_vaga": data.get("link_vaga"),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Dispara para o Webhook
                    resp_save = requests.post(MAKE_WEBHOOK_ANALISE_URL, json=payload_save)
                    
                    if resp_save.status_code == 200:
                        st.session_state.vaga_enviada = True
                        st.toast("🎉 Sucesso! Vaga catalogada no Notion.", icon="🚀")
                        st.rerun()
                    else:
                        st.error(f"Erro ao salvar no Notion: {resp_save.status_code}")
                except Exception as e:
                    st.error(f"Falha na comunicação de salvamento: {e}")
    else:
        st.success("✅ Esta vaga foi enviada para o Notion!")

# st.divider()

# --- SEÇÃO 2: BUSCADOR INTELIGENTE (INTACTO) ---
#st.markdown("### 🔍 Buscador de Vagas Inteligente")
#st.write("Diga ao agente que tipo de vaga você procura e ele fará uma varredura na web.")

#search_query = st.text_input(
#    "O que deseja buscar?", 
#    value="Buscar 3 vagas de Dev Júnior em Mogi das Cruzes ou Próximo"
#)

#if st.button("Buscar Vagas na Web"):
#    with st.spinner("Acionando Agente de Busca..."):
#        try:
#            search_payload = {
#                "source": "streamlit_search",
#                "termo_busca": search_query,
#                "timestamp": datetime.now().isoformat()
#            }
            
#            resp_busca = requests.post(MAKE_WEBHOOK_BUSCA_URL, json=search_payload)
            
#            if resp_busca.status_code == 200:
#                st.success(f"🔎 Busca por '{search_query}' iniciada! Você receberá os resultados no Telegram em instantes.")
#            else:
#                st.error(f"Erro ao acionar busca: {resp_busca.status_code}")
                
#        except Exception as e:
#            st.error(f"Falha na conexão com o buscador: {e}")