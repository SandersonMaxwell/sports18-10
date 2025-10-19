import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Limpeza de Planilhas", layout="wide")
st.title("🧹 Limpeza de Dados - Bet Analysis Consolidado")

st.write("""
Suba **3 planilhas de uma vez**, contendo as colunas:
**Bet Amount**, **Payout**, **Client ID**, **Event** e **Final Score**.
O sistema vai gerar uma tabela consolidada mostrando em quais **eventos** cada Client ID aparece.
""")

uploaded_files = st.file_uploader("Selecione as 3 planilhas", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 3:
    dfs = []
    client_events = {}

    # Processa cada planilha
    for file in uploaded_files:
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

        # Preenche valores vazios da coluna event com o evento principal da planilha (primeiro não nulo)
        if "event" in df.columns:
            main_event = df["event"].dropna().iloc[0] if not df["event"].dropna().empty else "Evento Desconhecido"
            df["event"] = df["event"].fillna(main_event)

        # Armazena para depois criar coluna Planilhas com evento
        for idx, row in df.iterrows():
            cid = row["client id"]
            evt = row["event"]
            if cid not in client_events:
                client_events[cid] = set()
            client_events[cid].add(evt)

        dfs.append(df)

    # Concatena todas as planilhas
    combined_df = pd.concat(dfs, ignore_index=True)

    # Cria coluna Planilhas (aqui com os eventos correspondentes)
    combined_df["Planilhas"] = combined_df["client id"].apply(lambda x: ", ".join(sorted(client_events[x])))

    # Ordena por Client ID
    combined_df = combined_df.sort_values(by="client id").reset_index(drop=True)

    st.subheader("✅ Tabela Consolidada com Eventos")
    st.dataframe(combined_df, use_container_width=True)

    # CSV para download
    csv_buffer = BytesIO()
    combined_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label="📥 Baixar CSV Consolidado",
        data=csv_buffer,
        file_name="tabela_consolidada_eventos.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor, envie exatamente **3 arquivos** para processar.")
