import streamlit as st
import pandas as pd
import io
import os

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

# Upload do arquivo modelo (Excel .xls ou .xlsx)
uploaded_modelo = st.file_uploader("Enviar planilha modelo (XLS ou XLSX)", type=["xls", "xlsx"])

if uploaded_csv and uploaded_modelo:
    with st.spinner("🔄 Convertendo arquivo, aguarde..."):
        # Ler CSV
        try:
            df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="utf-8")
        except:
            df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="latin1")

        # Ler Excel modelo (xls ou xlsx)
        try:
            # Detecta extensão para escolher engine
            if uploaded_modelo.name.endswith(".xls"):
                df_modelo = pd.read_excel(uploaded_modelo, engine="xlrd")
            else:  # xlsx
                df_modelo = pd.read_excel(uploaded_modelo, engine="openpyxl")
        except Exception as e:
            st.error(f"Erro ao ler a planilha modelo: {e}")
            st.stop()

        # Ajustar linhas do modelo conforme CSV
        df_final = df_modelo.iloc[:len(df_origem)].copy()

        # --- Mapeamentos ---
        df_final["Data de Competência"] = df_origem["Data de Criação"]
        df_final["Data de Vencimento"] = df_origem["Data de Criação"]
        df_final["Data de Pagamento"] = df_origem["Data de Criação"]
        df_final["Descrição"] = df_origem["Produto"]
        df_final["Valor"] = df_origem["Ganho Liquido"]
        df_final["Categoria"] = "11307 - Receita de Cursos"

        # Gerar XLSX em memória
        output = io.BytesIO()
        df_final.to_excel(output, index=False)
        output.seek(0)

    st.success("✅ Conversão concluída com sucesso!")
    st.balloons()

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
