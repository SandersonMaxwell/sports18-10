import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilhas", layout="wide")
st.title("🧹 Limpeza de Dados - Bet Analysis")

st.write("""
Suba **3 planilhas de uma vez**, contendo as colunas:
**Bet Amount**, **Payout**, **Client ID**, **Event** e **Final Score**.
O sistema vai identificar os IDs de clientes que aparecem em mais de uma planilha.
""")

uploaded_files = st.file_uploader("Selecione as 3 planilhas", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 3:
    dfs = []
    client_sets = []

    for file in uploaded_files:
        # Lê a planilha
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

        # Ordena por Client ID
        df = df.sort_values(by="client id").reset_index(drop=True)

        dfs.append(df)
        client_sets.append(set(df["client id"]))

        st.subheader(f"✅ Planilha: {file.name}")
        st.dataframe(df, use_container_width=True)

        # CSV para download individual
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        st.download_button(
            label=f"📥 Baixar {file.name} limpo",
            data=csv_buffer,
            file_name=f"{file.name.split('.')[0]}_limpo.csv",
            mime="text/csv"
        )

    # Comparação de Client ID
    all_clients = client_sets[0] | client_sets[1] | client_sets[2]
    common_all_three = client_sets[0] & client_sets[1] & client_sets[2]
    in_two_or_more = {cid for cid in all_clients if sum(cid in s for s in client_sets) >= 2}

    st.subheader("🟢 IDs presentes nas 3 planilhas")
    st.write(sorted(common_all_three))

    st.subheader("🟡 IDs presentes em 2 ou mais planilhas")
    st.write(sorted(in_two_or_more))

else:
    st.info("Por favor, envie exatamente **3 arquivos** para processar.")
