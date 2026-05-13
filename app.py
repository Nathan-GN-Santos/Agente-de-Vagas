import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(
    page_title="Agente de Candidaturas AI",
    page_icon="🤖",
    layout="wide"
)

# Estilização customizada via Markdown
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: Configurações do Perfil ---
st.sidebar.header("⚙️ Configurações do Perfil")

nivel_vaga = st.sidebar.selectbox(
    "Nível da Vaga",
    ["Estágio", "Júnior", "Pleno", "Sênior", "Especialista/Lead"]
)

tipo_contrato = st.sidebar.radio(
    "Tipo de Contrato",
    ["CLT", "PJ", "Temporário", "Freelance"]
)

preferencia_horario = st.sidebar.selectbox(
    "Preferência de Horário",
    ["Full-time (9h - 18h)", "Part-time", "Flexível", "Escala 12x36"]
)

st.sidebar.divider()
st.sidebar.info("As configurações acima serão enviadas junto com a descrição da vaga para análise.")

# --- ÁREA PRINCIPAL ---
st.title("🤖 Agente de Candidaturas Inteligente")
st.caption("Analise vagas e prepare sua candidatura em segundos.")

st.subheader("📝 Detalhes da Oportunidade")
conteudo_vaga = st.text_area(
    "Cole aqui a descrição completa da vaga (Job Description):",
    placeholder="Ex: Procuramos desenvolvedor Python com experiência em Django...",
    height=350
)

# Colunas para organizar o botão e o status
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🚀 Analisar Vaga"):
        if not conteudo_vaga.strip():
            st.warning("⚠️ Por favor, cole o conteúdo da vaga antes de analisar.")
        else:
            # Preparação do Payload
            payload = {
                "nivel": nivel_vaga,
                "contrato": tipo_contrato,
                "horario": preferencia_horario,
                "descricao_vaga": conteudo_vaga
            }

            webhook_url = "https://hook.us2.make.com/1b43sb1mff7qr8kpic4hlovkd1yzxjwh"
            with st.spinner("Enviando dados para o agente..."):
                try:
                    response = requests.post(
                        webhook_url, 
                        data=json.dumps(payload),
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Dados enviados com sucesso para o Make.com!")
                        st.balloons()
                    else:
                        st.error(f"❌ Erro no Webhook: {response.status_code}")
                
                except Exception as e:
                    st.error(f"🚨 Erro de conexão: {e}")

st.divider()
st.caption("Desenvolvido para acelerar sua entrada no mercado. 🚀")