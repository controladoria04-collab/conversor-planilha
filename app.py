# @title Conversor CSV -> Modelo | Automação 1.0

import pandas as pd
import io
from google.colab import files

print(">>> UPLOAD 1: Envie o CSV com os dados ORIGINAIS <<<")
uploaded_csv = files.upload()
if not uploaded_csv:
    raise ValueError("Nenhum arquivo CSV enviado.")
csv_name = next(iter(uploaded_csv))

# Tentativa de leitura do CSV
try:
    df_origem = pd.read_csv(io.BytesIO(uploaded_csv[csv_name]), encoding='utf-8', sep=';')
except:
    df_origem = pd.read_csv(io.BytesIO(uploaded_csv[csv_name]), encoding='latin1', sep=';')

print("\n>>> UPLOAD 2: Envie a PLANILHA MODELO (XLSX) <<<")
uploaded_model = files.upload()
if not uploaded_model:
    raise ValueError("Nenhuma planilha modelo enviada.")
model_name = next(iter(uploaded_model))

# Ler planilha modelo
df_modelo = pd.read_excel(io.BytesIO(uploaded_model[model_name]))

# Copiar e ajustar tamanho conforme o CSV
df_final = df_modelo.copy()
df_final = df_final.iloc[:len(df_origem)].copy()

# Mapeamentos solicitados
print("\nMapeando dados...")

# Datas — copiar Data de Criação para as 3 colunas
df_final["Data de Competência"] = df_origem["Data de Criação"]
df_final["Data de Vencimento"] = df_origem["Data de Criação"]
df_final["Data de Pagamento"] = df_origem["Data de Criação"]

# Descrição ← Produto
df_final["Descrição"] = df_origem["Produto"]

# Valor ← Ganho Liquido
df_final["Valor"] = df_origem["Ganho Liquido"]

# Categoria fixa
df_final["Categoria"] = "11307 - Receita de Cursos"

# Nome final do arquivo
out = "Planilha_Convertida.xlsx"
df_final.to_excel(out, index=False)

print("\n✔ Conversão concluída!")
print("Baixando arquivo final...")

files.download(out)
