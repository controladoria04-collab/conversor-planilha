import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(
    page_title="Conversor Conta Azul",
    page_icon="🔄",
    layout="centered"
)

# --- Título estilizado ---
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
        Conversor de Planilha
    </h1>
    <p style='text-align: center; font-size:18px;'>
        Envie o relatório do MyEduzz e receba a planilha formatada do Conta Azul.
    </p>
""", unsafe_allow_html=True)

st.info("📤 Envie o relatório do MyEduzz para iniciar a conversão.")

uploaded_csv = st.file_uploader("Enviar relatório do MyEduzz", type=["csv"])

MODEL_FILE = "modelo.xlsx"  # Coloque o modelo no mesmo diretório do app

if uploaded_csv:
    with st.spinner("🔄 Convertendo arquivo, aguarde..."):
        # Ler CSV
        try:
            df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="utf-8")
        except:
            df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="latin1")

        # Ler modelo Excel já presente
        try:
            if MODEL_FILE.endswith(".xls"):
                df_modelo = pd.read_excel(MODEL_FILE, engine="xlrd")
            else:
                df_modelo = pd.read_excel(MODEL_FILE, engine="openpyxl")
        except Exception as e:
            st.error(f"Erro ao ler a planilha modelo: {e}")
            st.stop()

        # Ajustar linhas do modelo conforme CSV
        df_final = df_modelo.iloc[:len(df_origem)].copy()

        # --- Mapeamentos ---
        # Converte para DATA (tipo date), sem hora, e mantém como data no Excel
        data_criacao_date = pd.to_datetime(
            df_origem["Data de Criação"],
            dayfirst=True,
            errors="coerce"
        ).dt.date  # <-- aqui vira "date" (não datetime e não texto)

        df_final["Data de Competência"] = data_criacao_date
        df_final["Data de Vencimento"]  = data_criacao_date
        df_final["Data de Pagamento"]   = data_criacao_date

        df_final["Descrição"] = df_origem["Produto"]
        df_final["Valor"] = df_origem["Ganho Liquido"]
        df_final["Categoria"] = "11307 - Receita de Cursos"

        # Gerar XLSX em memória e forçar formato dd/mm/aa nas colunas de data
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_final.to_excel(writer, index=False, sheet_name="Planilha")
            ws = writer.sheets["Planilha"]

            colunas_data = ["Data de Competência", "Data de Vencimento", "Data de Pagamento"]
            formato_excel = "DD/MM/YY"

            for nome_col in colunas_data:
                if nome_col in df_final.columns:
                    col_idx = df_final.columns.get_loc(nome_col) + 1  # 1-based no Excel
                    # Aplica formato nas células (linha 1 é cabeçalho)
                    for row in range(2, len(df_final) + 2):
                        ws.cell(row=row, column=col_idx).number_format = formato_excel

        output.seek(0)

    st.success("✅ Conversão concluída com sucesso!")

    st.download_button(
        label="📥 Baixar Planilha Convertida",
        data=output,
        file_name="Planilha_Convertida.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("""
    <br><br>
    <p style='text-align: center; color: #666; font-size:14px;'>
        “Entrega o teu caminho ao Senhor; confia nele, e o mais Ele fará.” — Salmo 37:5
    </p>
""", unsafe_allow_html=True)

