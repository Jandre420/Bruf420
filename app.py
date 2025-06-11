import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.markdown("""
    <style>
        .metric-card { background-color: #F9F9F9; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stTextInput > div > input { font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("consolidated_sales.xlsx")
    df.columns = df.columns.str.strip()
    df["Data de Emissão"] = pd.to_datetime(df["Data de Emissão"])
    return df

df = load_data()
total_vendas = len(df)
valor_total = df["Valor"].sum()
clientes_unicos = df["Código Cliente"].nunique()
ticket_medio = valor_total / clientes_unicos if clientes_unicos else 0

st.title("📊 Dashboard de Vendas")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Vendas", total_vendas)
col2.metric("Valor Total", f"R$ {valor_total:,.2f}")
col3.metric("Clientes Únicos", clientes_unicos)
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")
st.subheader("🔎 Buscar Vendas")
busca = st.text_input("Digite o código ou nome do cliente:")

if busca:
    filtro_df = df[df["Código Cliente"].astype(str).str.contains(busca, case=False) |
                   df["Nome Cliente"].astype(str).str.contains(busca, case=False)]
else:
    filtro_df = df.copy()

clientes, vendas = st.columns(2)
with clientes:
    st.markdown("#### Clientes")
    st.dataframe(filtro_df[["Código Cliente", "Nome Cliente"]].drop_duplicates(), use_container_width=True)
with vendas:
    st.markdown("#### Vendas")
    st.dataframe(filtro_df[["Data de Emissão", "Código Cliente", "Nome Cliente", "Valor"]].sort_values(by="Data de Emissão", ascending=False), use_container_width=True)

st.info("Para atualizar os dados, substitua o arquivo `consolidated_sales.xlsx`.")
