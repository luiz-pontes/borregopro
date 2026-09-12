import streamlit as st

# Configuração da página para modo amplo e título
st.set_page_config(
    page_title="MultVet - BorregoPRO",
    page_icon="🐏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo para ocultar a barra nativa superior do Streamlit (impede navegação para outros apps)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- SISTEMA DE AUTENTICAÇÃO / TRAVA DE SEGURANÇA ---
def checar_acesso():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acesso Restrito - MultVet BorregoPRO")
        st.write("Insira a senha de acesso enviada para o seu e-mail após a compra na Kiwify.")
        
        senha_digitada = st.text_input("Digite sua senha de acesso:", type="password")
        
        if st.button("Acessar Calculadora"):
            # VOCÊ PODE ALTERAR A SENHA ENTRE AS ASPAS ABAIXO:
            if senha_digitada == "BorregoPRO2026":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta. Verifique os dados recebidos na Kiwify.")
        return False
    return True

# --- APLICAÇÃO PRINCIPAL (SÓ CARREGA SE ESTIVER AUTENTICADO) ---
if checar_acesso():
    st.sidebar.title("MultVet BorregoPRO 🐏")
    st.sidebar.info("Calculadora e Gestão de Confinamento de Ovinos")
    
    if st.sidebar.button("Sair / Bloquear"):
        st.session_state["autenticado"] = False
        st.rerun()

    st.title("📊 Calculadora de Confinamento de Ovinos")
    st.write("BEM-VINDO AO BORREGOPRO - Insira os dados abaixo para calcular os resultados do seu lote.")

    # 1. Desempenho Animal
    st.subheader("1. Desempenho Animal")
    col1, col2 = st.columns(2)
    with col1:
        peso_inicial = st.number_input("Peso Inicial (kg):", value=18.0)
        peso_meta = st.number_input("Peso Meta de Abate (kg):", value=35.0)
    with col2:
        gmd = st.number_input("Ganho de Peso Esperado (g/dia):", value=250.0)
        consumo_ms = st.number_input("Consumo Estimado (% do Peso Vivo em MS):", value=3.5)

    # 2. Custo da Dieta e Resultados
    st.subheader("2. Custo da Dieta e Margem")
    col3, col4 = st.columns(2)
    with col3:
        custo_kg_racao = st.number_input("Custo do kg da Ração (R$):", value=1.80)
        preco_kg_carne = st.number_input("Preço de Venda do kg Vivo (R$):", value=12.00)
    with col4:
        # Cálculos Automáticos
        ganho_total_kg = peso_meta - peso_inicial
        dias_confinado = int(ganho_total_kg / (gmd / 1000)) if gmd > 0 else 0
        peso_medio = (peso_inicial + peso_meta) / 2
        consumo_diario_kg = peso_medio * (consumo_ms / 100)
        custo_alimentar_total = dias_confinado * consumo_diario_kg * custo_kg_racao
        receita_bruta = peso_meta * preco_kg_carne
        lucro_estimado = receita_bruta - custo_alimentar_total

    st.markdown("---")
    st.subheader("📈 Resumo do Lote")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Dias em Confinamento", f"{dias_confinado} dias")
    m2.metric("Consumo Total Ração/Cab", f"{round(dias_confinado * consumo_diario_kg, 1)} kg")
    m3.metric("Custo Alimentar/Cab", f"R$ {round(custo_alimentar_total, 2)}")
    m4.metric("Margem Bruta Estimada", f"R$ {round(lucro_estimado, 2)}")

    st.success("Cálculo realizado com sucesso! Para gerar o relatório em PDF, utilize o menu de impressão do navegador.")
