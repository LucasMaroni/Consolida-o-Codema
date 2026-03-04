import streamlit as st
import requests
import json
from datetime import datetime, date

# Configuração da página
st.set_page_config(
    page_title="Disparar Relatório CODEMA",
    page_icon="📊",
    layout="centered"
)

# URL do seu webhook do n8n (SUBSTITUA PELA SUA URL)
N8N_WEBHOOK_URL = "https://n8n.srv1162985.hstgr.cloud/webhook/CapaCodema"
# Ou se for local: "http://localhost:5678/webhook/disparar-relatorio"

def main():
    st.title("📊 Disparar Relatório CODEMA")
    st.markdown("---")
    
    st.markdown("""
    ### Preencha os parâmetros para gerar o relatório:
    """)
    
    # Formulário
    with st.form("form_relatorio"):
        col1, col2 = st.columns(2)
        
        with col1:
            data_inicio = st.date_input(
                "📅 Data de Início (Vencimento)",
                value=date.today(),
                format="DD/MM/YYYY"
            )
        
        with col2:
            data_fim = st.date_input(
                "📅 Data de Fim (Vencimento)",
                value=date.today(),
                format="DD/MM/YYYY"
            )
        
        proprietario = st.selectbox(
            "🏢 Proprietário",
            options=["TKS", "TRANSMARONI", "AMBOS"],
            index=2,  # AMBOS como padrão
            help="Selecione o proprietário para filtrar"
        )
        
        st.markdown("---")
        
        # Botão de submit
        submitted = st.form_submit_button(
            "🚀 Disparar Relatório",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validar datas
            if data_inicio > data_fim:
                st.error("❌ Data de início não pode ser maior que data de fim!")
                return
            
            # Preparar payload
            payload = {
                "dataInicio": data_inicio.strftime("%d/%m/%Y"),
                "dataFim": data_fim.strftime("%d/%m/%Y"),
                "proprietario": proprietario
            }
            
            # Mostrar payload em expander (debug)
            with st.expander("📦 Dados enviados"):
                st.json(payload)
            
            # Enviar para n8n com timeout de 60 segundos
            with st.spinner("🔄 Disparando workflow no n8n... (pode levar até 1 minuto)"):
                try:
                    # Aumentando o timeout para 60 segundos
                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=60  # ⬅️ ALTERADO PARA 60 SEGUNDOS
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Workflow disparado com sucesso!")
                        st.balloons()
                        
                        # Tenta mostrar resposta se houver
                        try:
                            resposta = response.json()
                            st.info("📋 Resposta do n8n:")
                            st.json(resposta)
                        except:
                            # Se não for JSON, mostra o texto
                            if response.text:
                                st.info("📋 Resposta do n8n:")
                                st.text(response.text)
                            
                    else:
                        st.error(f"❌ Erro ao disparar workflow: {response.status_code}")
                        st.text(response.text)
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Não foi possível conectar ao n8n. Verifique a URL do webhook.")
                except requests.exceptions.Timeout:
                    # Mensagem mais amigável para timeout
                    st.warning("⏳ O processo está demorando mais que 1 minuto...")
                    st.info("""
                    O workflow foi iniciado e continua processando em background no n8n.
                    
                    **O que fazer:**
                    - Aguarde alguns minutos e verifique se o relatório foi gerado
                    - Verifique os logs do n8n para confirmar a execução
                    - Se necessário, tente novamente com um período menor de datas
                    """)
                    
                    # Opção para tentar novamente
                    if st.button("🔄 Tentar novamente"):
                        st.rerun()
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Erro na requisição: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")

    # Informações adicionais
    st.markdown("---")
    with st.expander("ℹ️ Sobre"):
        st.markdown("""
        **Fluxo do n8n:**  
        Este formulário dispara o workflow que gera o relatório consolidado da CODEMA.
        
        **Parâmetros enviados:**
        - `dataInicio`: Data de início do período de vencimento
        - `dataFim`: Data de fim do período de vencimento
        - `proprietario`: Proprietário para filtro (TKS/TRANSMARONI/AMBOS)
        
        **⏱️ Timeout:**  
        O sistema aguarda até 1 minuto pela resposta do n8n. Se o processo demorar mais, o workflow continua em background.
        """)

if __name__ == "__main__":
    main()