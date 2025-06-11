import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.markdown("""
    <style>
        .metric-card { background-color: #F9F9F9; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("consolidated_sales.xlsx")
    df.columns = df.columns.str.strip()
    df["Data de Emissão"] = pd.to_datetime(df["Data de Emissão"])
    return df

df = load_data()
st.title("📊 Dashboard de Vendas")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Vendas", len(df))
col2.metric("Valor Total", f"R$ {df['Valor'].sum():,.2f}")
col3.metric("Clientes Únicos", df['Código Cliente'].nunique())
ticket_medio = df['Valor'].sum() / df['Código Cliente'].nunique()
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")
busca = st.text_input("Buscar Cliente ou Código:")
if busca:
    df_filtrado = df[df['Código Cliente'].astype(str).str.contains(busca, case=False) |
                     df['Nome Cliente'].astype(str).str.contains(busca, case=False)]
else:
    df_filtrado = df

st.dataframe(df_filtrado.sort_values("Data de Emissão", ascending=False), use_container_width=True)
