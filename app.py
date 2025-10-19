import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilhas", layout="wide")
st.title("🧹 Limpeza de Dados - Bet Analysis")

st.write("""
Faça upload de **uma planilha por vez** contendo as colunas:
**Bet Amount**, **Payout**, **Client ID**, **Event** e **Final Score**.
""")

uploaded_file = st.file_uploader("Selecione a planilha", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Mantém apenas as colunas desejadas
    expected_cols = ["Bet Amount", "Payout", "Client ID", "Event", "Final Score"]
    df = df[[col for col in expected_cols if col in df.columns]]

    # Ordena por Client ID
    df = df.sort_values(by="Client ID").reset_index(drop=True)

    st.subheader("✅ Dados Limpos da Planilha")
    st.dataframe(df, use_container_width=True)

    # Cria CSV para download
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.download_button(
        label="📥 Baixar CSV Limpo",
        data=csv_buffer,
        file_name=f"{uploaded_file.name.split('.')[0]}_limpo.csv",
        mime="text/csv"
    )
else:
    st.info("Envie uma planilha para processar.")
