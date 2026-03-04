import streamlit as st
import requests
from datetime import date

# Configuração da página - MAIS COMPACTA
st.set_page_config(
    page_title="CODEMA - Relatório",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS para reduzir espaçamentos e tornar mais compacto
st.markdown("""
<style>
    .main > div { padding: 1rem 1rem; }
    .stButton > button { margin-top: -10px; }
    div[data-testid="stForm"] { border: none; padding: 0; }
    .stAlert { margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# URL do webhook
N8N_WEBHOOK_URL = "https://n8n.srv1162985.hstgr.cloud/webhook/CapaCodema"

# Título principal
st.markdown("# 📄 CAPA CODEMA")

# Formulário compacto
with st.form("form"):
    cols = st.columns(2)
    with cols[0]:
        data_ini = st.date_input("📅 Data Início", date.today(), format="DD/MM/YYYY", label_visibility="collapsed")
    with cols[1]:
        data_fim = st.date_input("📅 Data Fim", date.today(), format="DD/MM/YYYY", label_visibility="collapsed")
    
    proprietario = st.selectbox(
        "👤 Proprietário", 
        ["TKS", "TRANSMARONI", "AMBOS"], 
        index=2,
        label_visibility="collapsed"
    )
    
    # Botão de envio (agora sem st.markdown extra)
    enviar = st.form_submit_button(
        "🚀 GERAR RELATÓRIO", 
        use_container_width=True, 
        type="primary"
    )

# Lógica de envio (fora do form para evitar duplicação)
if enviar:
    if data_ini > data_fim:
        st.error("❌ Data início > data fim")
    else:
        payload = {
            "dataInicio": data_ini.strftime("%d/%m/%Y"),
            "dataFim": data_fim.strftime("%d/%m/%Y"),
            "proprietario": proprietario
        }
        
        with st.spinner("⏳ Processando... até 3min"):
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=180  # ⏰ 3 MINUTOS!
                )
                
                if response.status_code == 200:
                    st.success("✅ Relatório disparado!")
                    st.balloons()
                    
                    # Mostra resposta resumida
                    try:
                        st.info(f"📋 {response.json().get('message', 'OK')}")
                    except:
                        pass
                else:
                    st.error(f"❌ Erro {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.warning("⏳ Processando em background (verifique e-mail/SharePoint em alguns minutos)")
            except Exception as e:
                st.error(f"❌ {str(e)[:50]}")
