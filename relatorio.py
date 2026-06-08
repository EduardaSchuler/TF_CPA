import os
import pandas as pd

PASTA_MICRODADOS = "microdados" 
ARQUIVO_FINAL_UNIFICADO = "encceja_rs_pronto_para_analise.csv"
SIGLA_ESTADO_ALVO = "RS"
anos_alvo = [2022, 2023, 2024]

COLUNAS_RELEVANTES = [
    'NU_ANO', 
    'TP_CERTIFICACAO', 
    'TP_FAIXA_ETARIA', 
    'TP_SEXO',
    'SG_UF_PROVA',
    'TP_PRESENCA_LC', 'TP_PRESENCA_CH', 'TP_PRESENCA_MT', 'TP_PRESENCA_CN',
    'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_MT', 'NU_NOTA_CN', 'NU_NOTA_REDACAO',
    'TP_STATUS_REDACAO',
    'Q01', 'Q02', 'Q03', 'Q04', 'Q05', 'Q06' 
]

print("Iniciando o processamento e extração de dados do Rio Grande do Sul...")
primeiro_bloco_geral = True

for arquivo in os.listdir(PASTA_MICRODADOS):
    if arquivo.endswith('.csv') and any(str(ano) in arquivo for ano in anos_alvo):
        caminho_completo = os.path.join(PASTA_MICRODADOS, arquivo)
        print(f"Lendo e filtrando: {arquivo}")
        
        for chunk in pd.read_csv(caminho_completo, sep=';', encoding='iso-8859-1', chunksize=100000, low_memory=False):
            # Remove possíveis espaços em branco invisíveis no nome das colunas
            chunk.columns = chunk.columns.str.strip()

            df_rs = chunk[chunk['SG_UF_PROVA'] == SIGLA_ESTADO_ALVO].copy()

            if not df_rs.empty:
                colunas_presentes = [col for col in COLUNAS_RELEVANTES if col in df_rs.columns]
                df_rs_filtrado = df_rs[colunas_presentes].copy()

                for col in df_rs_filtrado.columns:
                    if col.startswith('Q') or col == 'TP_SEXO':
                        df_rs_filtrado[col] = df_rs_filtrado[col].astype(str).str.strip()

                if primeiro_bloco_geral:
                    df_rs_filtrado.to_csv(ARQUIVO_FINAL_UNIFICADO, index=False, sep=';', encoding='utf-8')
                    primeiro_bloco_geral = False
                else:
                    df_rs_filtrado.to_csv(ARQUIVO_FINAL_UNIFICADO, index=False, sep=';', encoding='utf-8', mode='a', header=False)

print(f"\nConcluído com sucesso! Os dados relevantes do RS foram consolidados em: {ARQUIVO_FINAL_UNIFICADO}")
