import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Conversor Conta Azul",
    page_icon="🔄",
    layout="centered"
)

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


def parse_valor_robusto(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    s = s.str.replace("R$", "", regex=False).str.replace(" ", "", regex=False)

    tem_virgula = s.str.contains(",", na=False)
    tem_ponto = s.str.contains(r"\.", na=False)

    s2 = s.copy()

    # Ex: 1.234,56 -> 1234.56
    mask_ambos = tem_virgula & tem_ponto
    s2.loc[mask_ambos] = (
        s2.loc[mask_ambos]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    # Ex: 123,45 -> 123.45
    mask_so_virgula = tem_virgula & ~tem_ponto
    s2.loc[mask_so_virgula] = s2.loc[mask_so_virgula].str.replace(",", ".", regex=False)

    s2 = s2.str.replace(r"[^0-9\.\-]", "", regex=True)
    return pd.to_numeric(s2, errors="coerce")


if uploaded_csv:
    with st.spinner("🔄 Convertendo arquivo, aguarde..."):
        # Ler CSV
        try:
            df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="utf-8")
        except:
            df_origem = pd.read_csv(uploaded_csv, sep=";", encoding="latin1")

        # Ler modelo Excel já presente
        try:
            df_modelo = pd.read_excel(MODEL_FILE, engine="openpyxl")
        except Exception as e:
            st.error(f"Erro ao ler a planilha modelo: {e}")
            st.stop()

        # Ajustar linhas do modelo conforme CSV
        df_final = df_modelo.iloc[:len(df_origem)].copy()

        # --- Datas como DATA (sem hora) ---
        data_criacao_date = pd.to_datetime(
            df_origem["Data de Criação"],
            dayfirst=True,
            errors="coerce"
        ).dt.date

        df_final["Data de Competência"] = data_criacao_date
        df_final["Data de Vencimento"]  = data_criacao_date
        df_final["Data de Pagamento"]   = data_criacao_date

        # --- Valor como NÚMERO ---
        df_final["Valor"] = parse_valor_robusto(df_origem["Ganho Liquido"]).astype(float)

        df_final["Descrição"] = df_origem["Produto"]
        df_final["Categoria"] = "11307 - Receita de Cursos"

        # Gerar XLSX em memória e aplicar formatos
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_final.to_excel(writer, index=False, sheet_name="Planilha")
            ws = writer.sheets["Planilha"]

            # Formato das datas
            colunas_data = ["Data de Competência", "Data de Vencimento", "Data de Pagamento"]
            formato_data = "DD/MM/YY"
            for nome_col in colunas_data:
                if nome_col in df_final.columns:
                    col_idx = df_final.columns.get_loc(nome_col) + 1
                    for row in range(2, len(df_final) + 2):
                        ws.cell(row=row, column=col_idx).number_format = formato_data

            # Formato do valor + FORÇA o valor como número (evita "número armazenado como texto")
            if "Valor" in df_final.columns:
                col_valor = df_final.columns.get_loc("Valor") + 1
                formato_valor = "#,##0.00"

                valores = df_final["Valor"].tolist()
                for i, v in enumerate(valores, start=2):  # linha 1 é cabeçalho
                    cell = ws.cell(row=i, column=col_valor)
                    if pd.isna(v):
                        cell.value = None
                    else:
                        cell.value = float(v)  # <- garante número de verdade
                    cell.number_format = formato_valor

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
