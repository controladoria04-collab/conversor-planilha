import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Conversor CSV → Modelo", layout="centered")

st.title("Conversor CSV → Modelo | Automação 1.0")
st.write("Envie o arquivo **CSV original** e a **Planilha Modelo (XLSX)** para gerar a planilha final convertida.")


# ==============================================================
# UPLOAD DO CSV ORIGINAL
# ==============================================================
st.subheader("1️⃣ Envie o arquivo CSV original")
csv_file = st.file_uploader("Selecione o CSV", type=["csv"])

df_origem = None

if csv_file:
    # Tentativa de leitura em UTF-8 / Latin-1
    try:
        df_origem = pd.read_csv(csv_file, encoding="utf-8", sep=";")
    except:
        df_origem = pd.read_csv(csv_file, encoding="latin1", sep=";")

    st.success("CSV carregado com sucesso!")
    st.dataframe(df_origem.head())


# ==============================================================
# UPLOAD DA PLANILHA MODELO
# ==============================================================
st.subheader("2️⃣ Envie a Planilha Modelo (XLSX)")
modelo_file = st.file_uploader("Selecione a planilha modelo", type=["xls", "xlsx"])

df_modelo = None

if modelo_file:
    df_modelo = pd.read_excel(modelo_file)
    st.success("Modelo carregado!")
    st.dataframe(df_modelo.head())


# ==============================================================
# PROCESSAMENTO
# ==============================================================
if st.button("🔄 Converter Planilha"):

    if df_origem is None:
        st.error("Envie primeiro o arquivo CSV!")
    elif df_modelo is None:
        st.error("Envie primeiro a Planilha Modelo!")
    else:
        st.info("Processando dados...")

        # Copiar modelo e ajustar tamanho conforme CSV
        df_final = df_modelo.copy()
        df_final = df_final.iloc[:len(df_origem)].copy()

        # ================================
        # MAPEAMENTOS EXATOS DO SEU CÓDIGO
        # ================================

        # Datas
        df_final["Data de Competência"] = df_origem["Data de Criação"]
        df_final["Data de Vencimento"] = df_origem["Data de Criação"]
        df_final["Data de Pagamento"] = df_origem["Data de Criação"]

        # Descrição
        df_final["Descrição"] = df_origem["Produto"]

        # Valor
        df_final["Valor"] = df_origem["Ganho Liquido"]

        # Categoria fixa
        df_final["Categoria"] = "11307 - Receita de Cursos"

        # Resultado final
        buffer = io.BytesIO()
        df_final.to_excel(buffer, index=False)
        buffer.seek(0)

        st.success("✔ Conversão concluída!")

        st.download_button(
            label="📥 Baixar Planilha Convertida",
            data=buffer,
            file_name="Planilha_Convertida.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.dataframe(df_final.head())
