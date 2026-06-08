import numpy as np
import pandas as pd

arquivo_entrada = "encceja_rs_pronto_para_analise.csv"
arquivo_limpo = "encceja_rs_limpo_e_tratado.csv"

print("Iniciando o tratamento dos problemas identificados na base...")
df = pd.read_csv(arquivo_entrada, sep=';', low_memory=False)


# 1. TRATAMENTO DE VALORES FALTANTES

# Identificar quem faltou a TODAS as provas (Absenteísmo total)
# Se a presença for 0 em todas as 4 áreas, o candidato não compareceu ao exame
faltou_tudo = (
    (df['TP_PRESENCA_LC'] == 0) & 
    (df['TP_PRESENCA_CH'] == 0) & 
    (df['TP_PRESENCA_MT'] == 0) & 
    (df['TP_PRESENCA_CN'] == 0)
)

print(f"Total de inscritos analisados: {len(df)}")
print(f"Removendo {faltou_tudo.sum()} candidatos que faltaram a todas as provas (absenteísmo total).")

# Filtro: Mantemos apenas quem compareceu a pelo menos uma prova
df_presentes = df[~faltou_tudo].copy()

# Tratamento do Questionário Socioeconômico:
questoes_socioeconomicas = ['Q01', 'Q02', 'Q03', 'Q04', 'Q05', 'Q06']
for q in questoes_socioeconomicas:
    if q in df_presentes.columns:
        df_presentes[q] = df_presentes[q].astype(str).str.strip()
        df_presentes[q] = df_presentes[q].replace(['nan', '', 'None', 'NULO'], 'Não Declarado')


# 2. CORREÇÃO DE INCONSISTÊNCIAS

inconsistencia_idade = (df_presentes['TP_CERTIFICACAO'] == 2) & (df_presentes['TP_FAIXA_ETARIA'].isin([1, 2]))
print(f"Corrigindo {inconsistencia_idade.sum()} registros de menores de idade inscritos para Ensino Médio.")

df_presentes = df_presentes[~inconsistencia_idade].copy()

# Presença inconsistente: Marcou presença (1), mas a nota ficou nula (NaN)
provas = ['LC', 'CH', 'MT', 'CN']
for prova in provas:
    col_presenca = f'TP_PRESENCA_{prova}'
    col_nota = f'NU_NOTA_{prova}'
    
    condicao_erro = (df_presentes[col_presenca] == 1) & (df_presentes[col_nota].isna())
    df_presentes.loc[condicao_erro, col_nota] = 0.0


# 3. TRATAMENTO DE OUTLIERS E FILTROS DE ANÁLISE
# Redação: Se o status da redação for 4 (Anulada), a nota deve ser 0
df_presentes.loc[df_presentes['TP_STATUS_REDACAO'] == 4, 'NU_NOTA_REDACAO'] = 0.0

# Identificar Idades Extremas (Outliers demográficos)
print(f"Candidatos acima de 70 anos na base: {(df_presentes['TP_FAIXA_ETARIA'] == 20).sum()}")


# 4. SALVAR A BASE PRONTA PARA A EQUAÇÃO FINAL
df_presentes.to_csv(arquivo_limpo, index=False, sep=';', encoding='utf-8')
print(f"Base tratada e salva com sucesso em: {arquivo_limpo}")
print(f"Tamanho final da base para análise de desempenho: {df_presentes.shape[0]} linhas.")