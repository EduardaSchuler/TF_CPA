import os
import pandas as pd

PASTA_MICRODADOS = "microdados" 
ARQUIVO_FINAL_UNIFICADO = "encceja_rio_grande_do_sul_2022_2024.csv"
SIGLA_ESTADO_ALVO = "RS"
anos_alvo = [2022, 2023, 2024]

print("Iniciando o processamento dos arquivos do Rio Grande do Sul...")
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
                if primeiro_bloco_geral:
                    df_rs.to_csv(ARQUIVO_FINAL_UNIFICADO, index=False, sep=';', encoding='utf-8')
                    primeiro_bloco_geral = False
                else:
                    df_rs.to_csv(ARQUIVO_FINAL_UNIFICADO, index=False, sep=';', encoding='utf-8', mode='a', header=False)

print(f"\nConcluído com sucesso! Os dados do RS foram consolidados em: {ARQUIVO_FINAL_UNIFICADO}")

