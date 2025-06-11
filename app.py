import pandas as pd
import streamlit as st

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_excel("consolidated_sales.xlsx", sheet_name="Sheet1")
    df.columns = df.columns.str.strip()  # Limpar espaços em branco
    df['Data de Emissão'] = pd.to_datetime(df['Data de Emissão'])
    return df

df = load_data()

st.title("Acompanhamento de Pedidos por Cliente")

# Filtros
clientes = st.multiselect(
    "Selecione o(s) Cliente(s):",
    options=df['Código Cliente'].unique(),
    default=df['Código Cliente'].unique()
)

data_min = df['Data de Emissão'].min()
data_max = df['Data de Emissão'].max()
data_range = st.date_input("Intervalo de Datas:", [data_min, data_max])

# Aplicar filtros
filtro_df = df[
    df['Código Cliente'].isin(clientes) &
    (df['Data de Emissão'] >= pd.to_datetime(data_range[0])) &
    (df['Data de Emissão'] <= pd.to_datetime(data_range[1]))
]

# Exibir dados
st.subheader("Pedidos Filtrados")
st.dataframe(filtro_df)

# Total por cliente
st.subheader("Total de Pedidos por Cliente")
total_por_cliente = filtro_df.groupby('Código Cliente')['Valor'].sum().reset_index()
st.bar_chart(total_por_cliente.set_index('Código Cliente'))

# Total geral
st.metric("Valor Total dos Pedidos Filtrados", f"R$ {filtro_df['Valor'].sum():,.2f}")

# Instruções
st.info("Para adicionar novos dados, atualize a planilha 'consolidated_sales.xlsx' e recarregue a página.")
