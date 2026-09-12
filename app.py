import streamlit as st

# 1. Configuração da página e identidade visual
st.set_page_config(
    page_title="MultVet - BorregoPRO",
    page_icon="🐑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para Visual Rural (Tons de Verde, Terra e Ajuste de Fonte)
st.markdown("""
    <style>
    /* Fundo da página e fontes */
    .stApp {
        background-color: #f4f7f4;
    }
    
    /* Cabeçalhos e Títulos */
    h1, h2, h3 {
        color: #1e4620 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Ajuste no tamanho da fonte dos rótulos para caberem em 1 linha */
    div[data-testid="stWidgetLabel"] label p {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #1e4620 !important;
    }

    /* Botões em verde rural */
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton>button:hover {
        background-color: #1b5e20 !important;
        color: #e8f5e9 !important;
    }

    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. Controle de Acesso / Senha
SENHA_CORRETA = "borrego2026"

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔒 Acesso Restrito - MultVet BorregoPRO")
    st.write("Insira a senha de acesso enviada para o seu e-mail ou fornecida pela consultoria.")
    
    senha_digitada = st.text_input("Digite sua senha de acesso:", type="password")
    
    if st.button("Acessar Calculadora"):
        if senha_digitada == SENHA_CORRETA:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")
    st.stop()

# 3. Sidebar (Menu Lateral)
with st.sidebar:
    st.title("MultVet BorregoPRO 🐑")
    st.write("**Sistema de Gestão & Nutrição de Ovinos**")
    st.markdown("---")
    if st.button("Sair / Bloquear"):
        st.session_state["autenticado"] = False
        st.rerun()

# 4. Tela Principal
st.title("📊 Calculadora de Confinamento & Estrutura Dietética")
st.markdown("Insira os dados do lote, desempenho esperado e a proporção da dieta em Matéria Seca (MS).")

# Nota estratégica orientando o produtor
st.info("💡 **Atenção Produtor:** Os cálculos consideram o **peso médio individual por animal** (cabeça), e não a soma total do lote todo.")

st.markdown("---")

# Seção 1: Desempenho Animal
st.subheader("1. Desempenho e Consumo Individual (Por Cabeça)")
col1, col2 = st.columns(2)

with col1:
    peso_inicial = st.number_input("Peso Inicial Médio (kg/animal):", value=16.0, step=0.5)
    peso_meta = st.number_input("Peso Meta Médio (kg/animal):", value=40.0, step=0.5)

with col2:
    gpd = st.number_input("Ganho de Peso Esperado (g/dia):", value=280.0, step=10.0)
    consumo_ms_pct = st.number_input(
        "Consumo Estimado (% do Peso Vivo em MS):", 
        value=3.50, 
        step=0.1,
        help="Média de consumo diário em matéria seca em relação ao peso médio do animal."
    )

st.markdown("---")

# Seção 2: Divisão da Dieta (Volumoso vs. Concentrado)
st.subheader("2. Proporção da Dieta (Base em Matéria Seca - MS)")
st.caption("Ajuste a participação do volumoso e do concentrado na Matéria Seca total consumida.")

col3, col4 = st.columns(2)

with col3:
    pct_volumoso = st.slider("Volumoso na MS (%):", min_value=0, max_value=100, value=40, step=5)
    pct_concentrado = 100 - pct_volumoso
    st.info(f"🌿 **Volumoso:** {pct_volumoso}% da MS")

with col4:
    st.metric(label="🌾 Concentrado (% da MS calculada):", value=f"{pct_concentrado}%")
    st.caption("O percentual de concentrado é ajustado automaticamente para somar 100%.")

st.markdown("---")

# Seção 3: Custos dos Alimentos e Venda
st.subheader("3. Custos da Dieta e Preço de Venda")
col5, col6, col7 = st.columns(3)

with col5:
    custo_volumoso_kg = st.number_input(
        "Custo do Volumoso (R$/kg MN):", 
        value=0.30, 
        step=0.05,
        help="Preço por quilo em Matéria Natural (como fornecido no cocho)."
    )

with col6:
    custo_concentrado_kg = st.number_input(
        "Custo do Concentrado (R$/kg MN):", 
        value=2.80, 
        step=0.10,
        help="Preço por quilo da ração/concentrado em Matéria Natural."
    )

with col7:
    preco_venda_kg = st.number_input("Preço Venda Vivo (R$/kg):", value=12.00, step=0.50)

# 5. Cálculos da Simulação
st.markdown("---")
st.subheader("📈 Resultados da Simulação (Por Animal)")

if gpd > 0 and peso_meta > peso_inicial:
    ganho_total_kg = peso_meta - peso_inicial
    dias_confinamento = ganho_total_kg / (gpd / 1000)
    peso_medio = (peso_inicial + peso_meta) / 2
    
    # Consumo médio diário em MS
    consumo_diario_ms_total = peso_medio * (consumo_ms_pct / 100)
    consumo_ms_volumoso = consumo_diario_ms_total * (pct_volumoso / 100)
    consumo_ms_concentrado = consumo_diario_ms_total * (pct_concentrado / 100)
    
    # Exibição dos cards de resultado
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.metric("Dias em Confinamento", f"{int(dias_confinamento)} dias")
        st.metric("Peso Médio do Lote", f"{peso_medio:.2f} kg")
        
    with res_col2:
        st.metric("Consumo Diário MS Total", f"{consumo_diario_ms_total:.2f} kg MS/dia")
        st.write(f"• **Volumoso (MS):** {consumo_ms_volumoso:.2f} kg/dia")
        st.write(f"• **Concentrado (MS):** {consumo_ms_concentrado:.2f} kg/dia")
        
    with res_col3:
        ganho_financeiro = ganho_total_kg * preco_venda_kg
        st.metric("Valor Gerado por Cabeça", f"R$ {ganho_financeiro:.2f}")

else:
    st.warning("Verifique os valores informados de Peso Inicial, Peso Meta e Ganho de Peso Diário.")

st.markdown("---")
st.caption("📌 **Nota:** Esta ferramenta é uma simulação de desempenho baseada em consumo médio diário. Para lote fechado, multiplique o consumo pelo número total de animais.")
