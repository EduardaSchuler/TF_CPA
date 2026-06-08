import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# CONFIGURAÇÕES INICIAIS E MAPEAMENTO
# ==========================================
arquivo_limpo = "encceja_rs_limpo_e_tratado.csv"
arquivo_bruto_rs = "encceja_rs_pronto_para_analise.csv"

# Mapeamento padrão do questionário socioeconômico (Q04)
mapeamento_trabalho = {
    'A': 'Não Trabalha',
    'B': 'Não Trabalha',
    'C': 'Trabalha',
    'D': 'Trabalha',
    'Não Declarado': 'Não Declarado'
}

# Mapeamento aproximado de TP_FAIXA_ETARIA para idade real (ponto médio de cada faixa)
mapeamento_idades = {
    1: 16, 2: 17, 3: 18, 4: 19, 5: 20, 6: 21, 7: 22, 8: 23, 9: 24, 10: 25,
    11: 28,  # Centro da faixa 26 a 30
    12: 33,  # Centro da faixa 31 a 35
    13: 38,  # Centro da faixa 36 a 40
    14: 43,  # Centro da faixa 41 a 45
    15: 48,  # Centro da faixa 46 a 50
    16: 53,  # Centro da faixa 51 a 55
    17: 58,  # Centro da faixa 56 a 60
    18: 63,  # Centro da faixa 61 a 65
    19: 68,  # Centro da faixa 66 a 70
    20: 73   # Acima de 70 (estimado)
}

colunas_notas = {
    'NU_NOTA_LC': 'Linguagens',
    'NU_NOTA_CH': 'Ciências Humanas',
    'NU_NOTA_MT': 'Matemática',
    'NU_NOTA_CN': 'Ciências da Natureza',
    'NU_NOTA_REDACAO': 'Redação'
}


# ==========================================
# GRÁFICO 1: IMPACTO NO DESEMPENHO (PRESENTES)
# ==========================================
print("Processando Gráfico 1: Desempenho dos Presentes...")
df_presentes = pd.read_csv(arquivo_limpo, sep=';', low_memory=False)

df_presentes['SITUACAO_TRABALHO'] = df_presentes['Q04'].map(mapeamento_trabalho).fillna('Não Declarado')
df_analise_pres = df_presentes[df_presentes['SITUACAO_TRABALHO'].isin(['Trabalha', 'Não Trabalha'])].copy()

df_medias = df_analise_pres.groupby('SITUACAO_TRABALHO')[list(colunas_notas.keys())].mean().reset_index()
df_long = pd.melt(df_medias, id_vars='SITUACAO_TRABALHO', value_vars=list(colunas_notas.keys()),
                    var_name='Prova', value_name='Nota Média')
df_long['Prova'] = df_long['Prova'].map(colunas_notas)

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

grafico1 = sns.barplot(data=df_long, x='Prova', y='Nota Média', hue='SITUACAO_TRABALHO', palette='Set2')
plt.title('Impacto da Rotina de Trabalho no Desempenho do Encceja (Rio Grande do Sul)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Áreas do Conhecimento / Avaliações', fontsize=12, labelpad=10)
plt.ylabel('Nota Média (Pontuação TRI / Redação)', fontsize=12, labelpad=10)
plt.legend(title='Situação de Trabalho', loc='upper right')
plt.ylim(0, df_long['Nota Média'].max() + 50) 

for container in grafico1.containers:
    grafico1.bar_label(container, fmt='%.1f', padding=3, fontsize=10)

plt.tight_layout()
plt.savefig('impacto_trabalho_desempenho_encceja.png', dpi=300)
plt.show()


# ==========================================
# CARREGAMENTO DA BASE BRUTA PARA OS FALTANTES
# ==========================================
print("Carregando base unificada para mapear os faltantes...")
df_bruto = pd.read_csv(arquivo_bruto_rs, sep=';', low_memory=False)

faltou_tudo = (
    (df_bruto['TP_PRESENCA_LC'] == 0) & 
    (df_bruto['TP_PRESENCA_CH'] == 0) & 
    (df_bruto['TP_PRESENCA_MT'] == 0) & 
    (df_bruto['TP_PRESENCA_CN'] == 0)
)
df_faltantes = df_bruto[faltou_tudo].copy()


# ==========================================
# GRÁFICO 2: PERFIL DOS AUSENTES (ABSENTEÍSMO)
# ==========================================
print("Processando Gráfico 2: Perfil de Trabalho dos Ausentes...")
df_faltantes['Q04'] = df_faltantes['Q04'].astype(str).str.strip()
df_faltantes['SITUACAO_TRABALHO'] = df_faltantes['Q04'].map(mapeamento_trabalho).fillna('Não Declarado')
df_analise_abs = df_faltantes[df_faltantes['SITUACAO_TRABALHO'].isin(['Trabalha', 'Não Trabalha'])]

contagem_abs = df_analise_abs['SITUACAO_TRABALHO'].value_counts()

plt.figure(figsize=(8, 8))
cores = ['#ff9999','#66b3ff']
explode = (0.05, 0) 

plt.pie(
    contagem_abs, 
    labels=contagem_abs.index, 
    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*contagem_abs.sum()):,})'.replace(',', '.'),
    startangle=90, colors=cores, explode=explode, shadow=True,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)

centro_circulo = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centro_circulo)

plt.title('Perfil de Trabalho dos Candidatos Ausentes\n(Abstenção Total no Encceja RS)', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('perfil_trabalho_abstenção_encceja.png', dpi=300)
plt.show()


# ==========================================
# GRÁFICO 3: DISTRIBUIÇÃO E IDADE MÉDIA DOS FALTANTES
# ==========================================
print("Processando Gráfico 3: Idade Média dos Ausentes...")

if 'NU_IDADE' in df_faltantes.columns:
    df_faltantes['IDADE_ANALISE'] = pd.to_numeric(df_faltantes['NU_IDADE'], errors='coerce')
else:
    df_faltantes['IDADE_ANALISE'] = df_faltantes['TP_FAIXA_ETARIA'].map(mapeamento_idades)

df_idade_limpa = df_faltantes[df_faltantes['IDADE_ANALISE'].notna()].copy()
idade_media = df_idade_limpa['IDADE_ANALISE'].mean()

plt.figure(figsize=(10, 6))
sns.histplot(data=df_idade_limpa, x='IDADE_ANALISE', kde=True, color='#9b59b6', bins=20, element='step')
plt.axvline(idade_media, color='red', linestyle='--', linewidth=2, label=f'Idade Média: {idade_media:.1f} anos')

plt.title('Distribuição de Idade dos Candidatos Ausentes (Encceja RS)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Idade Estimada (Anos)', fontsize=12, labelpad=10)
plt.ylabel('Quantidade de Candidatos Faltantes', fontsize=12, labelpad=10)
plt.legend(fontsize=12)
plt.tight_layout()

plt.savefig('idade_media_abstencao_encceja.png', dpi=300)
plt.show()


# ==========================================
# GRÁFICO 4: TENDÊNCIA DE DESEMPENHO POR IDADE (NOVO)
# ==========================================
print("Processando Gráfico 4: Tendência de Desempenho por Idade...")

# Mapeando a idade na base dos presentes (quem de fato tem nota)
if 'NU_IDADE' in df_presentes.columns:
    df_presentes['IDADE_ANALISE'] = pd.to_numeric(df_presentes['NU_IDADE'], errors='coerce')
else:
    df_presentes['IDADE_ANALISE'] = df_presentes['TP_FAIXA_ETARIA'].map(mapeamento_idades)

# Agrupando a base de presentes pela Idade para tirar a média de cada nota
df_desempenho_idade = df_presentes.groupby('IDADE_ANALISE')[list(colunas_notas.keys())].mean().reset_index()

# Reestruturando para o formato longo aceito pelo Seaborn
df_long_idade = pd.melt(df_desempenho_idade, id_vars='IDADE_ANALISE', value_vars=list(colunas_notas.keys()),
                        var_name='Prova', value_name='Nota Média')
df_long_idade['Prova'] = df_long_idade['Prova'].map(colunas_notas)

plt.figure(figsize=(12, 6))

# Criando gráfico de linhas (uma para cada matéria/redação)
sns.lineplot(
    data=df_long_idade, 
    x='IDADE_ANALISE', 
    y='Nota Média', 
    hue='Prova', 
    marker='o', 
    linewidth=2.5
)

plt.title('Tendência de Desempenho por Idade no Encceja RS', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Idade Estimada do Candidato (Anos)', fontsize=12, labelpad=10)
plt.ylabel('Nota Média OBTIDA', fontsize=12, labelpad=10)
plt.legend(title='Avaliações', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xlim(15, 65) # Limita o eixo X para evitar distorções de idades raríssimas
plt.tight_layout()

plt.savefig('desempenho_por_idade_encceja.png', dpi=300)
plt.show()

print("\nProcessamento completo de todas as 4 análises!")
