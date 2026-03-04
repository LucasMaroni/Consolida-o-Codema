import streamlit as st
import requests
from datetime import date

# Configuração da página
st.set_page_config(
    page_title="CODEMA - Relatório",
    page_icon="📄",
    layout="centered"
)

# CSS personalizado para um visual mais clean
st.markdown("""
<style>
    /* Fonte mais elegante */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Reduzindo espaçamentos */
    .main > div {
        padding: 1rem 1.5rem;
    }
    
    /* Estilo para o título */
    .titulo-principal {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    /* Labels mais elegantes */
    .stDateInput label, .stSelectbox label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #64748B;
        margin-bottom: 0.2rem;
    }
    
    /* Botão estilizado */
    .stButton > button {
        background: #0F172A;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s;
        border: 1px solid #1E293B;
    }
    
    .stButton > button:hover {
        background: #1E293B;
        border: 1px solid #334155;
        color: white;
    }
    
    /* Caixas de input mais suaves */
    .stDateInput input, .stSelectbox select {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    
    /* Mensagens de sucesso personalizadas */
    .success-box {
        background: #F0FDF4;
        border: 1px solid #86EFAC;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #166534;
    }
    
    .success-box strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
        color: #14532D;
    }
    
    .success-box p {
        margin: 0.3rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Separador sutil */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# URL do webhook
N8N_WEBHOOK_URL = "https://n8n.srv1162985.hstgr.cloud/webhook/CapaCodema"

# Título principal
st.markdown('<div class="titulo-principal">📄 Capa CODEMA</div>', unsafe_allow_html=True)

# Formulário com labels visíveis
with st.form("form"):
    # Linha das datas com labels
    st.markdown("**Período de vencimento**")
    col1, col2 = st.columns(2)
    with col1:
        data_ini = st.date_input(
            "Data inicial",
            value=date.today(),
            format="DD/MM/YYYY",
            key="data_ini"
        )
    with col2:
        data_fim = st.date_input(
            "Data final", 
            value=date.today(),
            format="DD/MM/YYYY",
            key="data_fim"
        )
    
    st.markdown("**Proprietário**")
    proprietario = st.selectbox(
        "Selecione",
        ["TKS", "TRANSMARONI", "AMBOS"],
        index=2,
        label_visibility="visible",
        key="prop"
    )
    
    st.markdown("")  # Espaço sutil
    enviar = st.form_submit_button("📨 Gerar relatório", use_container_width=True)

# Lógica de envio
if enviar:
    if data_ini > data_fim:
        st.error("❌ Data inicial maior que data final")
    else:
        payload = {
            "dataInicio": data_ini.strftime("%d/%m/%Y"),
            "dataFim": data_fim.strftime("%d/%m/%Y"),
            "proprietario": proprietario
        }
        
        with st.spinner("⏳ Processando..."):
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=180
                )
                
                if response.status_code == 200:
                    # Mensagem de sucesso personalizada com HTML/CSS
                    st.markdown("""
                    <div class="success-box">
                        <strong>✅ Relatório gerado com sucesso!</strong>
                        <p>📧 Capa enviada para o e-mail do departamento</p>
                        <p>📁 Disponível na pasta do setor (ProTech - Relatório Diário)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                else:
                    st.error(f"❌ Erro {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.warning("⏳ O processamento continua em segundo plano")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)[:50]}")
