Projeto ENCCEJA - TF_CPA
========================

Objetivo
--------
Este repositório organiza a extração, tratamento, análise e visualização dos microdados do ENCCEJA para o Estado do Rio Grande do Sul. O trabalho segue, de forma prática, as etapas do processo de análise de dados (inspirado no CRISP-DM) para produzir bases tratadas, gráficos e um dashboard interativo.

Resumo das etapas (mapeamento CRISP-DM)
--------------------------------------
- Entendimento de negócio: definir objetivo de analisar desempenho e participação do ENCCEJA no RS (anos 2022–2024) e identificar variáveis relevantes para análise socioeconômica e de desempenho.
- Entendimento dos dados: os microdados são lidos por `relatorio.py`, que consolida arquivos CSV brutos em uma base unificada filtrada para o RS.
- Preparação dos dados: `limpezaDeDados.py` realiza limpeza, tratamento de faltantes, correção de inconsistências e produz a base tratada `encceja_rs_limpo_e_tratado.csv`.
- Modelagem / Análise: `analiseGrafica.py` gera gráficos estáticos (matplotlib/seaborn) que salvam imagens em `Resultados fase 2\` para análise visual e relatórios.
- Avaliação: os gráficos e métricas geradas são usados para avaliar padrão de ausências, variação por idade, diferenças por situação de trabalho e evolução temporal.
- Deploy / Visualização: `dashboard.py` constrói um aplicativo interativo com Dash/Plotly para explorar filtros, KPIs e gráficos dinamicamente.

Estrutura de arquivos
---------------------
- `relatorio.py`  : leitura e consolidação dos microdados do diretório `microdados` em `encceja_rs_pronto_para_analise.csv`.
- `limpezaDeDados.py` : tratamento da base unificada, limpeza de dados, remoção de registros inválidos e criação de `encceja_rs_limpo_e_tratado.csv`.
- `analiseGrafica.py` : scripts para geração de gráficos estáticos (salva PNG em `Resultados fase 2\`).
- `dashboard.py` : aplicação interativa em Dash para visualização exploratória.
- `encceja_rs_pronto_para_analise.csv` : base unificada (gerada por `relatorio.py`) — pode estar presente ou ser criada ao executar o script.
- `encceja_rs_limpo_e_tratado.csv` : base tratada (gerada por `limpezaDeDados.py`).
- `Resultados fase 2/` : diretório de saída com imagens geradas por `analiseGrafica.py`.

Dependências principais
-----------------------
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- dash

Instalação rápida
-----------------
1. Criar e ativar um ambiente virtual (recomendado):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Instalar dependências:

```bash
python -m pip install --upgrade pip
pip install pandas numpy matplotlib seaborn plotly dash
```

Execução sugerida (ordem)
------------------------
1. Consolidar microdados (gera `encceja_rs_pronto_para_analise.csv`):

```bash
python relatorio.py
```

2. Tratar os dados (gera `encceja_rs_limpo_e_tratado.csv`):

```bash
python limpezaDeDados.py
```

3. Gerar gráficos estáticos (salva imagens em `Resultados fase 2\`):

```bash
python analiseGrafica.py
```

4. Rodar o dashboard interativo:

```bash
python dashboard.py
```

Observações e cuidados
---------------------
- Os scripts esperam encontrar os microdados brutos dentro da pasta `microdados`. Verifique se os arquivos CSV existem e seguem o padrão de separador `;`.
- As leituras em `relatorio.py` usam encoding `iso-8859-1` para os arquivos originais; ao salvar as bases consolidadas e tratadas, o encoding usado é `utf-8`.
- `analiseGrafica.py` e `dashboard.py` dependem das colunas padronizadas presentes nas bases geradas por `relatorio.py` e `limpezaDeDados.py`.
- Como as bases já existem (os CSVs listados no repositório), os primeiros passos podem ser pulados e pode-se executar apenas os scripts de análise e visualização.

Extensões recomendadas para VS Code (opcional)
---------------------------------------------
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Jupyter (ms-toolsai.jupyter): se quiser executar trechos interativos
