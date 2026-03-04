import streamlit as st
import requests
from datetime import date

# Configuração da página
st.set_page_config(
    page_title="CODEMA - Relatório Consolidado",
    page_icon="📊",
    layout="centered"
)

# CSS personalizado para um visual mais moderno
st.markdown("""
<style>
    /* Estilo global */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }
    
    /* Container principal com efeito glassmorphism */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 1rem auto;
        max-width: 600px;
    }
    
    /* Título estilizado */
    .titulo-principal {
        background: linear-gradient(120deg, #2E3192, #1BFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        padding: 0;
    }
    
    /* Subtítulo */
    .subtitulo {
        color: #666;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 1rem;
    }
    
    /* Labels dos campos */
    .campo-label {
        color: #2E3192;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Botão estilizado */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Cards de mensagem */
    .success-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1a4731;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #059669;
        box-shadow: 0 5px 15px rgba(5, 150, 105, 0.2);
    }
    
    .info-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Ícones nos cards */
    .card-icon {
        font-size: 1.5rem;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    /* Alerta de erro */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
    }
</style>
""", unsafe_allow_html=True)

# URL do webhook
N8N_WEBHOOK_URL = "https://n8n.srv1162985.hstgr.cloud/webhook/CapaCodema"

# Container principal com efeito glass
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Título e subtítulo
st.markdown('<div class="titulo-principal">📄 CAPA CODEMA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Relatório de Consolidação de Notas Fiscais</div>', unsafe_allow_html=True)

# Formulário
with st.form("form_relatorio"):
    # Linha das datas com labels
    st.markdown('<div class="campo-label">📅 PERÍODO DE VENCIMENTO</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p style="margin-bottom:0; color:#666; font-size:0.8rem;">Data Início</p>', unsafe_allow_html=True)
        data_inicio = st.date_input(
            "",
            value=date.today(),
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<p style="margin-bottom:0; color:#666; font-size:0.8rem;">Data Fim</p>', unsafe_allow_html=True)
        data_fim = st.date_input(
            "",
            value=date.today(),
            format="DD/MM/YYYY",
            label_visibility="collapsed"
        )
    
    # Espaço
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Proprietário com label
    st.markdown('<div class="campo-label">🏢 PROPRIETÁRIO</div>', unsafe_allow_html=True)
    proprietario = st.selectbox(
        "",
        options=["TKS", "TRANSMARONI", "AMBOS"],
        index=2,
        label_visibility="collapsed",
        help="Selecione o proprietário para filtrar as notas"
    )
    
    # Espaço
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botão de submit
    submitted = st.form_submit_button(
        "🚀 GERAR RELATÓRIO CONSOLIDADO",
        use_container_width=True,
        type="primary"
    )

# Lógica de envio
if submitted:
    if data_inicio > data_fim:
        st.error("❌ Data de início não pode ser maior que data de fim!")
    else:
        payload = {
            "dataInicio": data_inicio.strftime("%d/%m/%Y"),
            "dataFim": data_fim.strftime("%d/%m/%Y"),
            "proprietario": proprietario
        }
        
        # Mostrar payload em card
        with st.expander("📋 Dados enviados", expanded=False):
            st.json(payload)
        
        # Spinner personalizado
        with st.spinner("⏳ Processando relatório... (pode levar até 3 minutos)"):
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=180
                )
                
                if response.status_code == 200:
                    # Card de sucesso personalizado
                    st.markdown("""
                    <div class="success-card">
                        <span class="card-icon">✅</span>
                        <strong style="font-size:1.2rem;">RELATÓRIO GERADO COM SUCESSO!</strong>
                        <hr style="margin:10px 0; opacity:0.3;">
                        <div style="margin-top:10px;">
                            <p>📧 <strong>Capa enviada para o e-mail do departamento</strong><br>
                            <small style="color:#1a4731;">nfe.manutencao@transmaroni.com.br</small></p>
                            <p>📁 <strong>Disponível na pasta do setor</strong><br>
                            <small style="color:#1a4731;">ProTech - Manutenção Corporativa > Relatório Diário 📈</small></p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    
                    # Mostra resposta do n8n se houver
                    try:
                        resposta = response.json()
                        if resposta:
                            st.markdown("""
                            <div class="info-card">
                                <span class="card-icon">ℹ️</span>
                                <strong>Status do workflow:</strong> Executado com sucesso
                            </div>
                            """, unsafe_allow_html=True)
                    except:
                        pass
                        
                elif response.status_code == 202:
                    st.warning("⏳ Relatório em processamento... Você receberá por e-mail em instantes")
                else:
                    st.error(f"❌ Erro {response.status_code} ao gerar relatório")
                    
            except requests.exceptions.Timeout:
                st.warning("""
                ⏳ **O processo está demorando mais que o esperado...**
                
                O relatório continua sendo gerado em background e será enviado por e-mail assim que pronto.
                
                📧 Verifique sua caixa de entrada em alguns minutos
                📁 Ou acesse diretamente na pasta do setor
                """)
            except requests.exceptions.ConnectionError:
                st.error("❌ Não foi possível conectar ao servidor. Verifique sua internet.")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)[:100]}")

# Fecha o container principal
st.markdown('</div>', unsafe_allow_html=True)

# Informações adicionais em um rodapé compacto
st.markdown("""
<div style="text-align:center; margin-top:1rem; color:#999; font-size:0.7rem;">
    <hr style="margin:10px 0; opacity:0.2;">
    <span>⚡ Relatório Consolidado CODEMA | Processamento em até 3 minutos</span>
</div>
""", unsafe_allow_html=True)
