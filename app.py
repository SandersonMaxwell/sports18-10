import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilhas", layout="wide")
st.title("🧹 Limpeza de Dados - Bet Analysis Consolidado")

st.write("""
Suba **3 planilhas de uma vez**, contendo as colunas:
**Bet Amount**, **Payout**, **Client ID**, **Event** e **Final Score**.
O sistema vai gerar uma tabela consolidada mostrando em quais planilhas cada Client ID aparece.
""")

uploaded_files = st.file_uploader("Selecione as 3 planilhas", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 3:
    dfs = []
    client_sets = []
    file_names = [file.name for file in uploaded_files]

    # Processa cada planilha
    for idx, file in enumerate(uploaded_files):
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Padroniza nomes das colunas
        df.columns = df.columns.str.strip().str.lower()

        # Mantém apenas as colunas desejadas
        expected_cols = ["bet amount", "payout", "client id", "event", "final score"]
        df = df[[col for col in expected_cols if col in df.columns]]

        # Limpa Client ID (remove vírgulas e espaços)
        if "client id" in df.columns:
            df["client id"] = df["client id"].astype(str).str.replace(",", "").str.strip()

        # Adiciona coluna com nome da planilha
        df["planilha"] = file.name

        dfs.append(df)
        client_sets.append(set(df["client id"]))

    # Concatena todas as planilhas
    combined_df = pd.concat(dfs, ignore_index=True)

    # Cria coluna extra indicando em quais planilhas cada Client ID aparece
    client_planilhas = {}
    for idx, s in enumerate(client_sets):
        for cid in s:
            if cid not in client_planilhas:
                client_planilhas[cid] = []
            client_planilhas[cid].append(file_names[idx])

    combined_df["Planilhas"] = combined_df["client id"].apply(lambda x: ", ".join(client_planilhas[x]))

    # Ordena por Client ID
    combined_df = combined_df.sort_values(by="client id").reset_index(drop=True)

    st.subheader("✅ Tabela Consolidada")
    st.dataframe(combined_df, use_container_width=True)

    # CSV para download
    csv_buffer = BytesIO()
    combined_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label="📥 Baixar CSV Consolidado",
        data=csv_buffer,
        file_name="tabela_consolidada.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor, envie exatamente **3 arquivos** para processar.")
