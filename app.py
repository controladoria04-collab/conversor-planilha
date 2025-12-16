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

# --- Caixa de informação ---
st.info("📤 Envie o relatório do MyEduzz para iniciar a conversão.")

# Upload do CSV
uploaded_csv = st.file_uploader("Enviar relatório do MyEduzz", type=["csv"])

# Caminho do arquivo modelo (já existente no app)
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
        # Converte "Data de Criação" para datetime e zera a hora (fica só a data)
        data_criacao = pd.to_datetime(
            df_origem["Data de Criação"],
            dayfirst=True,
            errors="coerce"
        ).dt.normalize()  # remove a hora (00:00:00)

        df_final["Data de Competência"] = data_criacao
        df_final["Data de Vencimento"] = data_criacao
        df_final["Data de Pagamento"] = data_criacao

        df_final["Descrição"] = df_origem["Produto"]
        df_final["Valor"] = df_origem["Ganho Liquido"]
        df_final["Categoria"] = "11307 - Receita de Cursos"

        # Gerar XLSX em memória (com formato dd/mm/aa)
        output = io.BytesIO()
        with pd.ExcelWriter(
            output,
            engine="openpyxl",
            date_format="DD/MM/YY",
            datetime_format="DD/MM/YY"
        ) as writer:
            df_final.to_excel(writer, index=False)

        output.seek(0)

    st.success("✅ Conversão concluída com sucesso!")

    # Botão de download
    st.download_button(
        label="📥 Baixar Planilha Convertida",
        data=output,
        file_name="Planilha_Convertida.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- RODAPÉ COM O VERSÍCULO ---
st.markdown("""
    <br><br>
    <p style='text-align: center; color: #666; font-size:14px;'>
        “Entrega o teu caminho ao Senhor; confia nele, e o mais Ele fará.” — Salmo 37:5
    </p>
""", unsafe_allow_html=True)
