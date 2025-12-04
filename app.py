import streamlit as st
import pandas as pd
import io

st.title("Conversor CSV → Planilha Modelo")
st.write("Envie seu arquivo CSV e receba a planilha formatada automaticamente.")

# Upload do CSV
uploaded_csv = st.file_uploader("Enviar CSV original", type=["csv"])

# Arquivo modelo embutido (você coloca no mesmo diretório do app)
MODEL_FILE = "modelo.xlsx"

if uploaded_csv:
    # Ler CSV
    try:
        df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="utf-8")
    except:
        df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="latin1")

    # Ler a planilha modelo
    df_modelo = pd.read_excel(MODEL_FILE, engine="openpyxl")

    
    # Ajustar tamanho
    df_final = df_modelo.copy()
    df_final = df_final.iloc[:len(df_origem)].copy()
    
    # Mapeamentos
    df_final["Data de Competência"] = df_origem["Data de Criação"]
    df_final["Data de Vencimento"] = df_origem["Data de Criação"]
    df_final["Data de Pagamento"] = df_origem["Data de Criação"]

    df_final["Descrição"] = df_origem["Produto"]
    df_final["Valor"] = df_origem["Ganho Liquido"]
    df_final["Categoria"] = "11307 - Receita de Cursos"

    # Converter para Excel em memória
    output = io.BytesIO()
    df_final.to_excel(output, index=False)
    output.seek(0)

    # Download
    st.success("Arquivo convertido com sucesso!")
    st.download_button(
        label="Baixar Planilha Convertida",
        data=output,
        file_name="Planilha_Convertida.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

