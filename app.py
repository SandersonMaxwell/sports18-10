import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Consolidado Client ID", layout="wide")
st.title("🧹 Consolidado de Client ID por Eventos")

st.write("""
Suba **3 planilhas de uma vez**, contendo as colunas:
**Client ID** e **Event**.
O sistema vai gerar uma tabela consolidada mostrando em quais **eventos** cada Client ID aparece.
""")

uploaded_files = st.file_uploader("Selecione as 3 planilhas", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) == 3:
    client_events = {}

    # Processa cada planilha
    for file in uploaded_files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Padroniza nomes das colunas
        df.columns = df.columns.str.strip().str.lower()

        # Mantém apenas Client ID e Event
        expected_cols = ["client id", "event"]
        df = df[[col for col in expected_cols if col in df.columns]]

        # Limpa Client ID
        df["client id"] = df["client id"].astype(str).str.replace(",", "").str.strip()

        # Preenche valores vazios de Event
        main_event = df["event"].dropna().iloc[0] if not df["event"].dropna().empty else "Evento Desconhecido"
        df["event"] = df["event"].fillna(main_event)

        # Armazena eventos por Client ID
        for idx, row in df.iterrows():
            cid = row["client id"]
            evt = row["event"]
            if cid not in client_events:
                client_events[cid] = set()
            client_events[cid].add(evt)

    # Cria tabela final
    final_df = pd.DataFrame({
        "Client ID": list(client_events.keys()),
        "Eventos": [", ".join(sorted(evts)) for evts in client_events.values()]
    })

    # Ordena por Client ID
    final_df = final_df.sort_values(by="Client ID").reset_index(drop=True)

    st.subheader("✅ Tabela Consolidada de Client ID")
    st.dataframe(final_df, use_container_width=True)

    # CSV para download
    csv_buffer = BytesIO()
    final_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label="📥 Baixar CSV Consolidado",
        data=csv_buffer,
        file_name="tabela_consolidada_client_id.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor, envie exatamente **3 arquivos** para processar.")
