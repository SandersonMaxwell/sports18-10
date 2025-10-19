import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilhas", layout="wide")

st.title("🧹 Limpeza de Dados - Bet Analysis")

st.write("""
Faça upload de **3 planilhas (.xlsx ou .csv)** contendo as colunas:
**Bet Amount**, **Payout**, **Client ID**, **Event** e **Final Score**.
""")

uploaded_files = st.file_uploader("Selecione as 3 planilhas", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 3:
    dfs = []
    for file in uploaded_files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Mantém apenas as colunas desejadas (caso existam)
        expected_cols = ["Bet Amount", "Payout", "Client ID", "Event", "Final Score"]
        df = df[[col for col in expected_cols if col in df.columns]]

        dfs.append(df)

    # Junta tudo
    combined_df = pd.concat(dfs, ignore_index=True)

    # Ordena por Client ID
    combined_df = combined_df.sort_values(by="Client ID").reset_index(drop=True)

    st.subheader("✅ Dados Limpos e Combinados")
    st.dataframe(combined_df, use_container_width=True)

    # Cria o CSV para download
    csv_buffer = BytesIO()
    combined_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.download_button(
        label="📥 Baixar CSV Limpo",
        data=csv_buffer,
        file_name="dados_limpos.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor, envie exatamente **3 arquivos** para processar.")
