import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilhas", layout="wide")
st.title("🧹 Limpeza de Dados - Bet Analysis")

st.write("""
Suba **3 planilhas, uma de cada vez**, contendo as colunas:
**Bet Amount**, **Payout**, **Client ID**, **Event** e **Final Score**.
O sistema vai identificar os IDs de clientes que aparecem em mais de uma planilha.
""")

# Lista para armazenar as planilhas
if "dataframes" not in st.session_state:
    st.session_state.dataframes = []

uploaded_file = st.file_uploader("Selecione uma planilha", type=["csv", "xlsx"])

if uploaded_file:
    # Lê a planilha
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Padroniza os nomes das colunas (remove espaços e deixa lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Colunas que queremos
    expected_cols = ["bet amount", "payout", "client id", "event", "final score"]
    
    # Mantém apenas as colunas que existem
    df = df[[col for col in expected_cols if col in df.columns]]

    # Ordena por Client ID
    df = df.sort_values(by="client id").reset_index(drop=True)

    st.subheader(f"✅ Dados limpos da planilha: {uploaded_file.name}")
    st.dataframe(df, use_container_width=True)

    # Salva na sessão
    st.session_state.dataframes.append(df)

    # Mostra botão para baixar essa planilha limpa
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label=f"📥 Baixar {uploaded_file.name} limpo",
        data=csv_buffer,
        file_name=f"{uploaded_file.name.split('.')[0]}_limpo.csv",
        mime="text/csv"
    )

# Quando tiver 3 planilhas carregadas
if len(st.session_state.dataframes) == 3:
    st.success("✅ As 3 planilhas foram carregadas!")

    # Lista de client IDs de cada planilha
    clients_lists = [set(df["client id"]) for df in st.session_state.dataframes]

    # Identifica os Client ID que aparecem em mais de uma planilha
    common_ids = clients_lists[0] & clients_lists[1] & clients_lists[2]  # IDs que aparecem em todas
    ids_2_or_more = (clients_lists[0] | clients_lists[1] | clients_lists[2]) - (clients_lists[0] ^ clients_lists[1] ^ clients_lists[2])  # IDs que aparecem em 2 ou mais planilhas

    st.subheader("🟢 IDs presentes nas 3 planilhas")
    st.write(sorted(common_ids))

    st.subheader("🟡 IDs presentes em 2 ou mais planilhas")
    st.write(sorted(ids_2_or_more))
