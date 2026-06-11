import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

arquivo_limpo = "encceja_rs_limpo_e_tratado.csv"
arquivo_bruto_rs = "encceja_rs_pronto_para_analise.csv"

mapeamento_trabalho = {
    "A": "Não Trabalha",
    "B": "Não Trabalha",
    "C": "Trabalha",
    "Não Declarado": "Não Declarado",
}

mapeamento_idades = {
    1: 16,
    2: 17,
    3: 18,
    4: 19,
    5: 20,
    6: 21,
    7: 22,
    8: 23,
    9: 24,
    10: 25,
    11: 28,  # Centro da faixa 26 a 30
    12: 33,  # Centro da faixa 31 a 35
    13: 38,  # Centro da faixa 36 a 40
    14: 43,  # Centro da faixa 41 a 45
    15: 48,  # Centro da faixa 46 a 50
    16: 53,  # Centro da faixa 51 a 55
    17: 58,  # Centro da faixa 56 a 60
    18: 63,  # Centro da faixa 61 a 65
    19: 68,  # Centro da faixa 66 a 70
    20: 73,  # Acima de 70 (estimado)
}

colunas_notas = {
    "NU_NOTA_LC": "Linguagens",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_CN": "Ciências da Natureza",
    "NU_NOTA_REDACAO": "Redação",
}

mapeamento_q01 = {
    "A": "Nunca estudou",
    "B": "Fund. Incompleto",
    "C": "Fund. Completo",
    "D": "Médio Completo",
    "E": "Superior Completo",
}

mapeamento_q05 = {
    "A": "Sem renda",
    "B": "Até ½ SM",
    "C": "½ a 1 SM",
    "D": "1 a 1,5 SM",
    "E": "1,5 a 2 SM",
    "F": "2 a 2,5 SM",
    "G": "2,5 a 3 SM",
    "H": "3 a 4 SM",
    "I": "4 a 5 SM",
    "J": "5 a 6 SM",
    "K": "Acima de 6 SM",
}

mapeamento_q06 = {
    "A": "Escola Pública",
    "B": "Escola Privada",
    "C": "Pública e Privada",
    "D": "Não Frequentou",
}

print("Processando Gráfico 1: Desempenho dos Presentes...")
df_presentes = pd.read_csv(arquivo_limpo, sep=";", low_memory=False)

df_presentes["SITUACAO_TRABALHO"] = (
    df_presentes["Q04"].map(mapeamento_trabalho).fillna("Não Declarado")
)
df_analise_pres = df_presentes[
    df_presentes["SITUACAO_TRABALHO"].isin(["Trabalha", "Não Trabalha"])
].copy()

df_medias = (
    df_analise_pres.groupby("SITUACAO_TRABALHO")[list(colunas_notas.keys())]
    .mean()
    .reset_index()
)
df_long = pd.melt(
    df_medias,
    id_vars="SITUACAO_TRABALHO",
    value_vars=list(colunas_notas.keys()),
    var_name="Prova",
    value_name="Nota Média",
)
df_long["Prova"] = df_long["Prova"].map(colunas_notas)

plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

grafico1 = sns.barplot(
    data=df_long, x="Prova", y="Nota Média", hue="SITUACAO_TRABALHO", palette="Set2"
)
plt.title(
    "Impacto da Rotina de Trabalho no Desempenho do Encceja (Rio Grande do Sul)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Áreas do Conhecimento / Avaliações", fontsize=12, labelpad=10)
plt.ylabel("Nota Média (Pontuação TRI / Redação)", fontsize=12, labelpad=10)
plt.legend(title="Situação de Trabalho", loc="upper right")
plt.ylim(0, df_long["Nota Média"].max() + 50)

for container in grafico1.containers:
    grafico1.bar_label(container, fmt="%.1f", padding=3, fontsize=10)

plt.tight_layout()
plt.savefig("Resultados fase 2\\impacto_trabalho_desempenho_encceja.png", dpi=300)
plt.show()

print("Carregando base unificada para mapear os faltantes...")
df_bruto = pd.read_csv(arquivo_bruto_rs, sep=";", low_memory=False)

faltou_tudo = (
    (df_bruto["TP_PRESENCA_LC"] == 0)
    & (df_bruto["TP_PRESENCA_CH"] == 0)
    & (df_bruto["TP_PRESENCA_MT"] == 0)
    & (df_bruto["TP_PRESENCA_CN"] == 0)
)
df_faltantes = df_bruto[faltou_tudo].copy()

print("Processando Gráfico 2: Perfil de Trabalho dos Ausentes...")
df_faltantes["Q04"] = df_faltantes["Q04"].astype(str).str.strip()
df_faltantes["SITUACAO_TRABALHO"] = (
    df_faltantes["Q04"].map(mapeamento_trabalho).fillna("Não Declarado")
)
df_analise_abs = df_faltantes[
    df_faltantes["SITUACAO_TRABALHO"].isin(["Trabalha", "Não Trabalha"])
]

contagem_abs = df_analise_abs["SITUACAO_TRABALHO"].value_counts()

plt.figure(figsize=(8, 8))
cores = ["#ff9999", "#66b3ff"]
explode = (0.05, 0)

plt.pie(
    contagem_abs,
    labels=contagem_abs.index,
    autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100.*contagem_abs.sum()):,})".replace(
        ",", "."
    ),
    startangle=90,
    colors=cores,
    explode=explode,
    shadow=True,
    textprops={"fontsize": 12, "fontweight": "bold"},
)

centro_circulo = plt.Circle((0, 0), 0.70, fc="white")
fig = plt.gcf()
fig.gca().add_artist(centro_circulo)

plt.title(
    "Perfil de Trabalho dos Candidatos Ausentes\n(Abstenção Total no Encceja RS)",
    fontsize=14,
    fontweight="bold",
    pad=20,
)
plt.tight_layout()
plt.savefig("Resultados fase 2\\perfil_trabalho_abstencao_encceja.png", dpi=300)
plt.show()

print("Processando Gráfico 3: Idade Média dos Ausentes...")

if "NU_IDADE" in df_faltantes.columns:
    df_faltantes["IDADE_ANALISE"] = pd.to_numeric(
        df_faltantes["NU_IDADE"], errors="coerce"
    )
else:
    df_faltantes["IDADE_ANALISE"] = df_faltantes["TP_FAIXA_ETARIA"].map(
        mapeamento_idades
    )

df_idade_limpa = df_faltantes[df_faltantes["IDADE_ANALISE"].notna()].copy()
idade_media = df_idade_limpa["IDADE_ANALISE"].mean()

plt.figure(figsize=(10, 6))
sns.histplot(
    data=df_idade_limpa,
    x="IDADE_ANALISE",
    kde=True,
    color="#9b59b6",
    bins=20,
    element="step",
)
plt.axvline(
    idade_media,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Idade Média: {idade_media:.1f} anos",
)

plt.title(
    "Distribuição de Idade dos Candidatos Ausentes (Encceja RS)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Idade Estimada (Anos)", fontsize=12, labelpad=10)
plt.ylabel("Quantidade de Candidatos Faltantes", fontsize=12, labelpad=10)
plt.legend(fontsize=12)
plt.tight_layout()

plt.savefig("Resultados fase 2\\idade_media_abstencao_encceja.png", dpi=300)
plt.show()

print("Processando Gráfico 4: Tendência de Desempenho por Idade...")

if "NU_IDADE" in df_presentes.columns:
    df_presentes["IDADE_ANALISE"] = pd.to_numeric(
        df_presentes["NU_IDADE"], errors="coerce"
    )
else:
    df_presentes["IDADE_ANALISE"] = df_presentes["TP_FAIXA_ETARIA"].map(
        mapeamento_idades
    )

df_desempenho_idade = (
    df_presentes.groupby("IDADE_ANALISE")[list(colunas_notas.keys())]
    .mean()
    .reset_index()
)

df_long_idade = pd.melt(
    df_desempenho_idade,
    id_vars="IDADE_ANALISE",
    value_vars=list(colunas_notas.keys()),
    var_name="Prova",
    value_name="Nota Média",
)
df_long_idade["Prova"] = df_long_idade["Prova"].map(colunas_notas)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=df_long_idade,
    x="IDADE_ANALISE",
    y="Nota Média",
    hue="Prova",
    marker="o",
    linewidth=2.5,
)

plt.title(
    "Tendência de Desempenho por Idade no Encceja RS",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Idade Estimada do Candidato (Anos)", fontsize=12, labelpad=10)
plt.ylabel("Nota Média OBTIDA", fontsize=12, labelpad=10)
plt.legend(title="Avaliações", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xlim(15, 65)
plt.tight_layout()

plt.savefig("Resultados fase 2\\desempenho_por_idade_encceja.png", dpi=300)
plt.show()

print("Processando Gráfico 5: Evolução Temporal das Notas...")

df_temporal = df_bruto.dropna(subset=list(colunas_notas.keys()), how="all").copy()

df_medias_ano = (
    df_temporal.groupby("NU_ANO")[list(colunas_notas.keys())].mean().reset_index()
)
df_long_ano = pd.melt(
    df_medias_ano,
    id_vars="NU_ANO",
    value_vars=list(colunas_notas.keys()),
    var_name="Prova",
    value_name="Nota Média",
)
df_long_ano["Prova"] = df_long_ano["Prova"].map(colunas_notas)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(
    "Evolução Temporal do Encceja RS (2022–2024)",
    fontsize=15,
    fontweight="bold",
    y=1.02,
)

notas_tri = ["Linguagens", "Ciências Humanas", "Matemática", "Ciências da Natureza"]
df_tri = df_long_ano[df_long_ano["Prova"].isin(notas_tri)]

sns.lineplot(
    ax=axes[0],
    data=df_tri,
    x="NU_ANO",
    y="Nota Média",
    hue="Prova",
    marker="o",
    linewidth=2.5,
)
axes[0].set_title("Provas Objetivas (Escala TRI)", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Ano", fontsize=11)
axes[0].set_ylabel("Nota Média", fontsize=11)
axes[0].set_xticks([2022, 2023, 2024])
axes[0].legend(title="Área", loc="lower right")

for line in axes[0].lines:
    xdata, ydata = line.get_xdata(), line.get_ydata()
    for x, y in zip(xdata, ydata):
        axes[0].annotate(
            f"{y:.1f}",
            xy=(x, y),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

df_redacao = df_long_ano[df_long_ano["Prova"] == "Redação"]

sns.lineplot(
    ax=axes[1],
    data=df_redacao,
    x="NU_ANO",
    y="Nota Média",
    marker="o",
    linewidth=2.5,
    color="#e74c3c",
    label="Redação",
)
axes[1].set_title("Redação (Escala 0–10)", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Ano", fontsize=11)
axes[1].set_ylabel("Nota Média", fontsize=11)
axes[1].set_xticks([2022, 2023, 2024])
axes[1].set_ylim(0, 10)
axes[1].legend(title="Avaliação")

for line in axes[1].lines:
    xdata, ydata = line.get_xdata(), line.get_ydata()
    for x, y in zip(xdata, ydata):
        axes[1].annotate(
            f"{y:.2f}",
            xy=(x, y),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=10,
        )

plt.tight_layout()
plt.savefig("evolucao_temporal_notas_encceja.png", dpi=300)
plt.show()

print("  -> Subgráfico: Taxa de participação por ano...")
cols_presenca = ["TP_PRESENCA_LC", "TP_PRESENCA_CH", "TP_PRESENCA_MT", "TP_PRESENCA_CN"]
nomes_presenca = {
    "TP_PRESENCA_LC": "Linguagens",
    "TP_PRESENCA_CH": "Ciências Humanas",
    "TP_PRESENCA_MT": "Matemática",
    "TP_PRESENCA_CN": "Ciências da Natureza",
}

taxas = []
for ano in [2022, 2023, 2024]:
    df_ano = df_bruto[df_bruto["NU_ANO"] == ano]
    for col in cols_presenca:
        validos = df_ano[col].notna()
        taxa = (df_ano.loc[validos, col] == 1).sum() / validos.sum() * 100
        taxas.append(
            {
                "Ano": ano,
                "Prova": nomes_presenca[col],
                "Taxa de Presença (%)": round(taxa, 1),
            }
        )

df_taxas = pd.DataFrame(taxas)

plt.figure(figsize=(11, 5))
grafico_pres = sns.barplot(
    data=df_taxas, x="Prova", y="Taxa de Presença (%)", hue="Ano", palette="Blues_d"
)
plt.title(
    "Taxa de Participação por Área e Ano (Encceja RS)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Área do Conhecimento", fontsize=12, labelpad=10)
plt.ylabel("Candidatos Presentes (%)", fontsize=12, labelpad=10)
plt.ylim(0, 55)
plt.legend(title="Ano")

for container in grafico_pres.containers:
    grafico_pres.bar_label(container, fmt="%.1f%%", padding=3, fontsize=9)

plt.tight_layout()
plt.savefig("Resultados fase 2\\participacao_por_ano_encceja.png", dpi=300)
plt.show()


print("Processando Gráfico 6: Perfil Socioeconômico x Desempenho...")

df_socio = df_presentes.copy()

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle(
    "Perfil Socioeconômico x Desempenho no Encceja RS",
    fontsize=15,
    fontweight="bold",
    y=1.02,
)

df_socio["Q05_LABEL"] = df_socio["Q05"].astype(str).str.strip().map(mapeamento_q05)
df_socio["NOTA_MEDIA_GERAL"] = df_socio[
    ["NU_NOTA_LC", "NU_NOTA_CH", "NU_NOTA_MT", "NU_NOTA_CN"]
].mean(axis=1)

ordem_renda = list(mapeamento_q05.values())
df_renda = (
    df_socio[df_socio["Q05_LABEL"].notna()]
    .groupby("Q05_LABEL")["NOTA_MEDIA_GERAL"]
    .mean()
    .reindex(ordem_renda)
    .reset_index()
)
df_renda.columns = ["Renda Familiar", "Nota Média Geral"]

sns.barplot(
    ax=axes[0],
    data=df_renda,
    x="Nota Média Geral",
    y="Renda Familiar",
    color="orange",
    orient="h",
)

axes[0].set_title("Renda Familiar (Q05)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Nota Média (TRI)", fontsize=10)
axes[0].set_ylabel("")
for bar in axes[0].patches:
    w = bar.get_width()
    axes[0].text(
        w + 0.3, bar.get_y() + bar.get_height() / 2, f"{w:.1f}", va="center", fontsize=8
    )

df_socio["Q01_LABEL"] = df_socio["Q01"].astype(str).str.strip().map(mapeamento_q01)

notas_obj = ["NU_NOTA_LC", "NU_NOTA_CH", "NU_NOTA_MT", "NU_NOTA_CN"]
nomes_obj = ["Linguagens", "C. Humanas", "Matemática", "C. Natureza"]

ordem_esc = list(mapeamento_q01.values())
df_escol = (
    df_socio[df_socio["Q01_LABEL"].notna()]
    .groupby("Q01_LABEL")[notas_obj]
    .mean()
    .reindex(ordem_esc)
    .reset_index()
)
df_escol.columns = ["Escolaridade da Mãe"] + nomes_obj

df_long_escol = pd.melt(
    df_escol,
    id_vars="Escolaridade da Mãe",
    value_vars=nomes_obj,
    var_name="Área",
    value_name="Nota Média",
)

sns.lineplot(
    ax=axes[1],
    data=df_long_escol,
    x="Escolaridade da Mãe",
    y="Nota Média",
    hue="Área",
    marker="o",
    linewidth=2,
)
axes[1].set_title("Escolaridade da Mãe (Q01)", fontsize=12, fontweight="bold")
axes[1].set_xlabel("")
axes[1].set_ylabel("Nota Média (TRI)", fontsize=10)
axes[1].tick_params(axis="x", rotation=20)
axes[1].legend(title="Área", fontsize=8, title_fontsize=9)

# --- Painel 3: Tipo de Escola (Q06) x Nota de Redação ---
df_socio["Q06_LABEL"] = df_socio["Q06"].astype(str).str.strip().map(mapeamento_q06)

df_escola_tipo = df_socio[
    df_socio["Q06_LABEL"].notna() & df_socio["NU_NOTA_REDACAO"].notna()
].copy()

ordem_escola = list(mapeamento_q06.values())
sns.boxplot(
    ax=axes[2],
    data=df_escola_tipo,
    x="Q06_LABEL",
    y="NU_NOTA_REDACAO",
    order=ordem_escola,
    color="orange",
)
axes[2].set_title("Tipo de Escola (Q06) x Redação", fontsize=12, fontweight="bold")
axes[2].set_xlabel("")
axes[2].set_ylabel("Nota de Redação (0–10)", fontsize=10)
axes[2].tick_params(axis="x", rotation=15)

plt.tight_layout()
plt.savefig("Resultados fase 2\\socioeconomico_desempenho_encceja.png", dpi=300)
plt.show()


print("\nProcessamento completo de todas as 6 análises!")
print("Arquivos gerados:")
graficos = [
    "impacto_trabalho_desempenho_encceja.png",
    "perfil_trabalho_abstencao_encceja.png",
    "idade_media_abstencao_encceja.png",
    "desempenho_por_idade_encceja.png",
    "evolucao_temporal_notas_encceja.png",
    "participacao_por_ano_encceja.png",
    "socioeconomico_desempenho_encceja.png",
]
for g in graficos:
    print(f"  - {g}")
