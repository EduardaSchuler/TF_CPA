import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

arquivo_limpo = "encceja_rs_limpo_e_tratado.csv"
arquivo_pronto = "encceja_rs_pronto_para_analise.csv"

COR_AZUL = "#005CAB"
COR_AZUL_C = "#2BABE2"
COR_LARANJA = "#F7931E"
COR_AMARELO = "#FBB03B"
COR_VERDE = "#39B54A"
COR_ROXO = "#9B59B6"
COR_CINZA_BG = "#f0f2f5"
COR_SIDEBAR = "#0A2A4A"

PALETA = [COR_AZUL, COR_LARANJA, COR_VERDE, COR_AMARELO, COR_ROXO]

print("Carregando dados...")
df_pres = pd.read_csv(arquivo_limpo, sep=";", low_memory=False)
df_bruto = pd.read_csv(arquivo_pronto, sep=";", low_memory=False)

MAP_TRABALHO = {
    "A": "Não Trabalha",
    "B": "Não Trabalha",
    "C": "Trabalha",
    "D": "Trabalha",
}
MAP_IDADES = {
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
    11: 28,
    12: 33,
    13: 38,
    14: 43,
    15: 48,
    16: 53,
    17: 58,
    18: 63,
    19: 68,
    20: 73,
}
MAP_Q01 = {
    "A": "Nunca estudou",
    "B": "Fund. Incompleto",
    "C": "Fund. Completo",
    "D": "Médio Completo",
    "E": "Superior Completo",
}
MAP_Q05 = {
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
MAP_Q06 = {
    "A": "Escola Pública",
    "B": "Escola Privada",
    "C": "Pública e Privada",
    "D": "Não Frequentou",
}

COLS_NOTAS = {
    "NU_NOTA_LC": "Linguagens",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_CN": "Ciências da Natureza",
    "NU_NOTA_REDACAO": "Redação",
}
NOTAS_OBJ = ["NU_NOTA_LC", "NU_NOTA_CH", "NU_NOTA_MT", "NU_NOTA_CN"]
NOMES_OBJ = ["Linguagens", "C. Humanas", "Matemática", "C. Natureza"]
TODAS_AREAS = list(COLS_NOTAS.values())

ORDEM_RENDA = list(MAP_Q05.values())
ORDEM_ESC = list(MAP_Q01.values())
ORDEM_ESCOLA = list(MAP_Q06.values())
ANOS_DISP = sorted(df_bruto["NU_ANO"].dropna().unique().tolist())

df_pres["SITUACAO_TRABALHO"] = df_pres["Q04"].map(MAP_TRABALHO).fillna("Não Declarado")
df_pres["Q01_LABEL"] = df_pres["Q01"].astype(str).str.strip().map(MAP_Q01)
df_pres["Q05_LABEL"] = df_pres["Q05"].astype(str).str.strip().map(MAP_Q05)
df_pres["Q06_LABEL"] = df_pres["Q06"].astype(str).str.strip().map(MAP_Q06)
df_pres["NOTA_GERAL"] = df_pres[NOTAS_OBJ].mean(axis=1)
df_pres["IDADE_ANALISE"] = df_pres["TP_FAIXA_ETARIA"].map(MAP_IDADES)

df_bruto["Q05_LABEL"] = df_bruto["Q05"].astype(str).str.strip().map(MAP_Q05)
df_bruto["NOTA_GERAL"] = df_bruto[NOTAS_OBJ].mean(axis=1)
df_bruto["IDADE_ANALISE"] = df_bruto["TP_FAIXA_ETARIA"].map(MAP_IDADES)

FALTOU_TUDO = (
    (df_bruto["TP_PRESENCA_LC"] == 0)
    & (df_bruto["TP_PRESENCA_CH"] == 0)
    & (df_bruto["TP_PRESENCA_MT"] == 0)
    & (df_bruto["TP_PRESENCA_CN"] == 0)
)

CARD = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.09)",
}


def filtro_bar(page_id, mostrar_areas=False):
    children = [
        html.Span(
            "🔎 Filtros",
            style={
                "fontWeight": "bold",
                "color": COR_AZUL,
                "fontSize": "13px",
                "whiteSpace": "nowrap",
            },
        ),
        html.Div(
            [
                html.Label(
                    "Ano",
                    style={
                        "fontSize": "11px",
                        "color": "#888",
                        "display": "block",
                        "marginBottom": "3px",
                    },
                ),
                dcc.Checklist(
                    id=f"ano-{page_id}",
                    options=[{"label": f" {a}", "value": a} for a in ANOS_DISP],
                    value=ANOS_DISP,
                    inline=True,
                    inputStyle={"marginRight": "3px", "accentColor": COR_AZUL},
                    labelStyle={"marginRight": "10px", "fontSize": "12px"},
                ),
            ]
        ),
        html.Div(
            [
                html.Label(
                    "Sexo",
                    style={
                        "fontSize": "11px",
                        "color": "#888",
                        "display": "block",
                        "marginBottom": "3px",
                    },
                ),
                dcc.Checklist(
                    id=f"sexo-{page_id}",
                    options=[
                        {"label": " Feminino", "value": "F"},
                        {"label": " Masculino", "value": "M"},
                    ],
                    value=["F", "M"],
                    inline=True,
                    inputStyle={"marginRight": "3px", "accentColor": COR_AZUL},
                    labelStyle={"marginRight": "10px", "fontSize": "12px"},
                ),
            ]
        ),
        html.Div(
            [
                html.Label(
                    "Certificação",
                    style={
                        "fontSize": "11px",
                        "color": "#888",
                        "display": "block",
                        "marginBottom": "3px",
                    },
                ),
                dcc.Checklist(
                    id=f"cert-{page_id}",
                    options=[
                        {"label": " E. Médio", "value": 2},
                        {"label": " E. Fundamental", "value": 1},
                    ],
                    value=[1, 2],
                    inline=True,
                    inputStyle={"marginRight": "3px", "accentColor": COR_AZUL},
                    labelStyle={"marginRight": "10px", "fontSize": "12px"},
                ),
            ]
        ),
    ]
    if mostrar_areas:
        children.append(
            html.Div(
                [
                    html.Label(
                        "Áreas",
                        style={
                            "fontSize": "11px",
                            "color": "#888",
                            "display": "block",
                            "marginBottom": "3px",
                        },
                    ),
                    dcc.Checklist(
                        id="areas-temporal",
                        options=[{"label": f" {a}", "value": a} for a in TODAS_AREAS],
                        value=TODAS_AREAS,
                        inline=True,
                        inputStyle={"marginRight": "3px", "accentColor": COR_VERDE},
                        labelStyle={"marginRight": "10px", "fontSize": "12px"},
                    ),
                ]
            )
        )
    return html.Div(
        style={
            **CARD,
            "display": "flex",
            "gap": "24px",
            "alignItems": "center",
            "flexWrap": "wrap",
            "marginBottom": "20px",
            "padding": "12px 18px",
            "borderLeft": f"5px solid {COR_AZUL_C}",
        },
        children=children,
    )


def kpi_box(titulo, valor, cor):
    return html.Div(
        style={**CARD, "textAlign": "center", "padding": "18px"},
        children=[
            html.P(
                titulo,
                style={
                    "margin": "0",
                    "color": "#888",
                    "fontSize": "12px",
                    "fontWeight": "600",
                },
            ),
            html.H2(
                valor,
                style={
                    "margin": "6px 0 0 0",
                    "color": cor,
                    "fontSize": "26px",
                    "fontWeight": "800",
                },
            ),
        ],
    )


def titulo_pagina(icone, titulo, subtitulo, cor=COR_AZUL):
    return html.Div(
        style={"marginBottom": "20px"},
        children=[
            html.H2(
                f"{icone} {titulo}",
                style={
                    "margin": "0 0 4px 0",
                    "color": cor,
                    "fontSize": "20px",
                    "fontWeight": "800",
                },
            ),
            html.P(
                subtitulo, style={"margin": "0", "color": "#666", "fontSize": "13px"}
            ),
            html.Hr(
                style={
                    "border": "none",
                    "borderTop": f"3px solid {cor}",
                    "margin": "10px 0 0 0",
                }
            ),
        ],
    )


def vazio():
    return go.Figure().update_layout(
        template="plotly_white",
        annotations=[
            {
                "text": "Sem dados para a seleção",
                "showarrow": False,
                "font": {"size": 14, "color": "#999"},
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
            }
        ],
    )


def fp(anos, sexos, certs, df):
    d = df.copy()
    if anos:
        d = d[d["NU_ANO"].isin(anos)]
    if sexos:
        d = d[d["TP_SEXO"].isin(sexos)]
    if certs:
        d = d[d["TP_CERTIFICACAO"].isin(certs)]
    return d


PAGINAS = [
    ("visao-geral", "Visão Geral"),
    ("absenteismo", "Absenteísmo"),
    ("faixa-etaria", "Faixa Etária"),
    ("temporal", "Evolução Temporal"),
    ("socioeconomico", "Impacto Socioeconômico"),
]


def nav_link(page_id, icone, label, ativo):
    bg = COR_AZUL_C if ativo else "transparent"
    fw = "700" if ativo else "400"
    return html.A(
        href=f"/{page_id}",
        style={
            "display": "block",
            "padding": "11px 18px",
            "borderRadius": "6px",
            "marginBottom": "4px",
            "backgroundColor": bg,
            "color": "white",
            "textDecoration": "none",
            "fontSize": "13px",
            "fontWeight": fw,
            "letterSpacing": "0.3px",
        },
        children=f"{icone}  {label}",
    )


def sidebar(pagina_atual):
    return html.Div(
        style={
            "width": "200px",
            "minWidth": "200px",
            "backgroundColor": COR_SIDEBAR,
            "padding": "20px 12px",
            "borderRadius": "10px",
            "height": "fit-content",
            "position": "sticky",
            "top": "20px",
        },
        children=[
            html.Div(
                "ENCCEJA RS",
                style={
                    "color": "white",
                    "fontWeight": "800",
                    "fontSize": "15px",
                    "marginBottom": "6px",
                    "letterSpacing": "1px",
                },
            ),
            html.Div(
                "Dashboard",
                style={
                    "color": COR_AZUL_C,
                    "fontSize": "11px",
                    "marginBottom": "20px",
                    "letterSpacing": "0.5px",
                },
            ),
            html.Hr(
                style={
                    "border": "none",
                    "borderTop": "1px solid #1e4070",
                    "marginBottom": "16px",
                }
            ),
            *[nav_link(pid, ic, lb, pid == pagina_atual) for pid, ic, lb in PAGINAS],
        ],
    )

def pagina_visao_geral():
    return html.Div(
        [
            titulo_pagina(
                "Visão Geral",
                "Panorama geral dos inscritos, presença e desempenho médio",
            ),
            filtro_bar("vg"),
            html.Div(
                id="kpi-vg",
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(4,1fr)",
                    "gap": "15px",
                    "marginBottom": "24px",
                },
            ),
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "20px",
                },
                children=[
                    html.Div(style=CARD, children=[dcc.Graph(id="vg-barras-notas")]),
                    html.Div(style=CARD, children=[dcc.Graph(id="vg-pizza-cert")]),
                ],
            ),
        ]
    )

def pagina_absenteismo():
    return html.Div(
        [
            titulo_pagina(
                "Absenteísmo",
                "Quem faltou, por quê, e qual o perfil dos ausentes",
                cor=COR_LARANJA,
            ),
            filtro_bar("ab"),
            html.Div(
                id="kpi-ab",
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(3,1fr)",
                    "gap": "15px",
                    "marginBottom": "24px",
                },
            ),
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "20px",
                    "marginBottom": "20px",
                },
                children=[
                    html.Div(style=CARD, children=[dcc.Graph(id="ab-pizza-trabalho")]),
                    html.Div(
                        style=CARD, children=[dcc.Graph(id="ab-trabalho-desempenho")]
                    ),
                ],
            ),
        ]
    )

def pagina_faixa_etaria():
    return html.Div(
        [
            titulo_pagina(
                "Faixa Etária",
                "Distribuição de idade dos ausentes e desempenho por idade",
                cor=COR_ROXO,
            ),
            filtro_bar("fe"),
            html.Div(
                style={**CARD, "marginBottom": "20px"},
                children=[dcc.Graph(id="fe-histograma")],
            ),
            html.Div(style=CARD, children=[dcc.Graph(id="fe-desempenho-idade")]),
        ]
    )

def pagina_temporal():
    return html.Div(
        [
            titulo_pagina(
                "Evolução Temporal",
                "Como notas e participação variaram de 2022 a 2024",
                cor=COR_VERDE,
            ),
            filtro_bar("tp", mostrar_areas=True),
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "2fr 1fr",
                    "gap": "20px",
                    "marginBottom": "20px",
                },
                children=[
                    html.Div(style=CARD, children=[dcc.Graph(id="tp-tri")]),
                    html.Div(style=CARD, children=[dcc.Graph(id="tp-redacao")]),
                ],
            ),
            html.Div(style=CARD, children=[dcc.Graph(id="tp-participacao")]),
        ]
    )


def pagina_socioeconomico():
    return html.Div(
        [
            titulo_pagina(
                "Impacto Socioeconômico nas Notas",
                "Questão de negócio: o perfil socioeconômico determina o desempenho dos candidatos?",
                cor="#8E44AD",
            ),
            filtro_bar("se"),
            html.Div(
                style={"marginBottom": "8px"},
                children=[
                    html.H3(
                        "Renda Familiar × Desempenho",
                        style={
                            "color": "#8E44AD",
                            "margin": "0 0 4px 0",
                            "fontSize": "15px",
                        },
                    ),
                    html.P(
                        "Candidatos de maior renda obtêm notas consistentemente maiores?",
                        style={
                            "color": "#888",
                            "fontSize": "12px",
                            "margin": "0 0 12px 0",
                        },
                    ),
                ],
            ),
            html.Div(
                style={**CARD, "marginBottom": "24px"},
                children=[dcc.Graph(id="se-renda")],
            ),
            html.Div(
                style={"marginBottom": "8px"},
                children=[
                    html.H3(
                        "Escolaridade da Mãe × Desempenho por Área",
                        style={
                            "color": "#8E44AD",
                            "margin": "0 0 4px 0",
                            "fontSize": "15px",
                        },
                    ),
                    html.P(
                        "Nível de instrução familiar influencia qual área do conhecimento?",
                        style={
                            "color": "#888",
                            "fontSize": "12px",
                            "margin": "0 0 12px 0",
                        },
                    ),
                ],
            ),
            html.Div(
                style={**CARD, "marginBottom": "24px"},
                children=[dcc.Graph(id="se-escolaridade")],
            ),
            # Bloco 3: Tipo de escola
            html.Div(
                style={"marginBottom": "8px"},
                children=[
                    html.H3(
                        "Tipo de Escola Frequentada × Redação",
                        style={
                            "color": "#8E44AD",
                            "margin": "0 0 4px 0",
                            "fontSize": "15px",
                        },
                    ),
                    html.P(
                        "Escola pública ou privada faz diferença na nota de redação?",
                        style={
                            "color": "#888",
                            "fontSize": "12px",
                            "margin": "0 0 12px 0",
                        },
                    ),
                ],
            ),
            html.Div(style=CARD, children=[dcc.Graph(id="se-escola-box")]),
        ]
    )

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard ENCCEJA RS"

app.layout = html.Div(
    style={
        "backgroundColor": COR_CINZA_BG,
        "fontFamily": "Segoe UI, sans-serif",
        "minHeight": "100vh",
        "padding": "20px",
    },
    children=[
        dcc.Location(id="url", refresh=False),
        # Cabeçalho fixo
        html.Div(
            style={
                "textAlign": "center",
                "backgroundColor": COR_AZUL,
                "color": "white",
                "padding": "18px",
                "borderRadius": "10px",
                "marginBottom": "20px",
            },
            children=[
                html.H1(
                    "Dashboard Encceja — Rio Grande do Sul",
                    style={
                        "margin": "0 0 4px 0",
                        "fontSize": "22px",
                        "fontWeight": "800",
                    },
                ),
                html.P(
                    "Análise de Absenteísmo, Desempenho e Impacto Socioeconômico",
                    style={"margin": "0", "opacity": "0.8", "fontSize": "12px"},
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "gap": "20px", "alignItems": "flex-start"},
            children=[
                html.Div(id="sidebar-container"),
                html.Div(id="page-content", style={"flex": "1", "minWidth": "0"}),
            ],
        ),
    ],
)

@app.callback(
    Output("sidebar-container", "children"),
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def rotear(pathname):
    rota = (pathname or "/").strip("/") or "visao-geral"
    paginas_map = {
        "visao-geral": pagina_visao_geral,
        "absenteismo": pagina_absenteismo,
        "faixa-etaria": pagina_faixa_etaria,
        "temporal": pagina_temporal,
        "socioeconomico": pagina_socioeconomico,
    }
    fn = paginas_map.get(rota, pagina_visao_geral)
    return sidebar(rota), fn()

@app.callback(
    Output("kpi-vg", "children"),
    Output("vg-barras-notas", "figure"),
    Output("vg-pizza-cert", "figure"),
    Input("ano-vg", "value"),
    Input("sexo-vg", "value"),
    Input("cert-vg", "value"),
)
def cb_vg(anos, sexos, certs):
    db = fp(anos, sexos, certs, df_bruto)
    dp = fp(anos, sexos, certs, df_pres)
    falt = db[FALTOU_TUDO.reindex(db.index, fill_value=False)]

    kpis = [
        kpi_box("Inscritos", f"{len(db):,}".replace(",", "."), COR_AZUL_C),
        kpi_box("Presentes", f"{len(dp):,}".replace(",", "."), COR_VERDE),
        kpi_box("Ausentes", f"{len(falt):,}".replace(",", "."), COR_LARANJA),
        kpi_box(
            "Taxa de Abstenção",
            f"{len(falt)/len(db)*100:.1f}%" if len(db) else "—",
            COR_LARANJA,
        ),
    ]

    medias = {COLS_NOTAS[c]: dp[c].mean() for c in COLS_NOTAS if dp[c].notna().any()}
    fig_bar = px.bar(
        x=list(medias.keys()),
        y=list(medias.values()),
        text=[f"{v:.1f}" for v in medias.values()],
        color=list(medias.keys()),
        color_discrete_sequence=PALETA,
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>Nota Média: <b>%{y:.1f}</b><extra></extra>"
    )
    fig_bar.update_layout(
        title="Nota Média por Área (Presentes)",
        xaxis_title="",
        yaxis_title="Nota Média",
        template="plotly_white",
        showlegend=False,
    )

    cert_cnt = (
        db["TP_CERTIFICACAO"]
        .map({1: "E. Fundamental", 2: "E. Médio"})
        .value_counts()
        .reset_index()
    )
    fig_pie = px.pie(
        cert_cnt,
        values="count",
        names="TP_CERTIFICACAO",
        hole=0.55,
        color_discrete_sequence=[COR_AZUL, COR_AZUL_C],
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value:,} inscritos (%{percent})<extra></extra>",
    )
    fig_pie.update_layout(
        title="Inscritos por Tipo de Certificação", template="plotly_white"
    )
    return kpis, fig_bar, fig_pie


@app.callback(
    Output("kpi-ab", "children"),
    Output("ab-pizza-trabalho", "figure"),
    Output("ab-trabalho-desempenho", "figure"),
    Input("ano-ab", "value"),
    Input("sexo-ab", "value"),
    Input("cert-ab", "value"),
)
def cb_ab(anos, sexos, certs):
    db = fp(anos, sexos, certs, df_bruto)
    dp = fp(anos, sexos, certs, df_pres)

    mask = FALTOU_TUDO.reindex(db.index, fill_value=False)
    falt = db[mask].copy()
    falt["Q04"] = falt["Q04"].astype(str).str.strip()
    falt["SITUACAO_TRABALHO"] = falt["Q04"].map(MAP_TRABALHO).fillna("Não Declarado")

    taxa = len(falt) / len(db) * 100 if len(db) else 0
    kpis = [
        kpi_box("Total Ausentes", f"{len(falt):,}".replace(",", "."), COR_LARANJA),
        kpi_box("Taxa de Abstenção", f"{taxa:.1f}%", COR_LARANJA),
        kpi_box("Presentes Efetivos", f"{len(dp):,}".replace(",", "."), COR_VERDE),
    ]

    cnt = (
        falt[falt["SITUACAO_TRABALHO"].isin(["Trabalha", "Não Trabalha"])][
            "SITUACAO_TRABALHO"
        ]
        .value_counts()
        .reset_index()
    )
    if cnt.empty:
        fig_pie = vazio()
    else:
        fig_pie = px.pie(
            cnt,
            values="count",
            names="SITUACAO_TRABALHO",
            hole=0.6,
            color_discrete_sequence=[COR_LARANJA, COR_AZUL],
        )
        fig_pie.update_traces(
            textinfo="percent+value",
            hovertemplate="<b>%{label}</b><br>%{value:,} ausentes<extra></extra>",
        )
        fig_pie.update_layout(
            title="Perfil de Trabalho dos Ausentes", template="plotly_white"
        )

    dp2 = dp[dp["SITUACAO_TRABALHO"].isin(["Trabalha", "Não Trabalha"])].copy()
    if dp2.empty:
        fig_bar = vazio()
    else:
        med = (
            dp2.groupby("SITUACAO_TRABALHO")[list(COLS_NOTAS.keys())]
            .mean()
            .reset_index()
        )
        lng = pd.melt(
            med,
            id_vars="SITUACAO_TRABALHO",
            value_vars=list(COLS_NOTAS.keys()),
            var_name="Prova",
            value_name="Nota Média",
        )
        lng["Prova"] = lng["Prova"].map(COLS_NOTAS)
        fig_bar = px.bar(
            lng,
            x="Prova",
            y="Nota Média",
            color="SITUACAO_TRABALHO",
            barmode="group",
            text_auto=".1f",
            color_discrete_map={"Não Trabalha": COR_AZUL_C, "Trabalha": COR_LARANJA},
            labels={"SITUACAO_TRABALHO": "Situação"},
        )
        fig_bar.update_traces(
            hovertemplate="<b>%{x}</b><br>%{fullData.name}<br>Nota: <b>%{y:.1f}</b><extra></extra>"
        )
        fig_bar.update_layout(
            title="Desempenho: Trabalhadores vs Não Trabalhadores",
            xaxis_title="",
            yaxis_title="Nota Média",
            template="plotly_white",
        )
    return kpis, fig_pie, fig_bar

@app.callback(
    Output("fe-histograma", "figure"),
    Output("fe-desempenho-idade", "figure"),
    Input("ano-fe", "value"),
    Input("sexo-fe", "value"),
    Input("cert-fe", "value"),
)
def cb_fe(anos, sexos, certs):
    db = fp(anos, sexos, certs, df_bruto)
    dp = fp(anos, sexos, certs, df_pres)

    mask = FALTOU_TUDO.reindex(db.index, fill_value=False)
    falt = db[mask].copy()
    falt["IDADE_ANALISE"] = falt["TP_FAIXA_ETARIA"].map(MAP_IDADES)
    df_ok = falt[falt["IDADE_ANALISE"].notna()]

    if df_ok.empty:
        fig_hist = vazio()
    else:
        media = df_ok["IDADE_ANALISE"].mean()
        fig_hist = px.histogram(
            df_ok,
            x="IDADE_ANALISE",
            nbins=25,
            color_discrete_sequence=[COR_ROXO],
            marginal="box",
        )
        fig_hist.add_vline(
            x=media,
            line_dash="dash",
            line_color=COR_VERDE,
            annotation_text=f"Média: {media:.1f} anos",
            annotation_position="top right",
        )
        fig_hist.update_traces(
            hovertemplate="Idade: <b>%{x}</b><br>Faltantes: <b>%{y}</b><extra></extra>",
            selector={"type": "histogram"},
        )
        fig_hist.update_layout(
            title="Distribuição Etária dos Faltantes",
            xaxis_title="Idade Estimada",
            yaxis_title="Total de Ausentes",
            template="plotly_white",
        )

    if dp.empty:
        fig_linha = vazio()
    else:
        desemp = (
            dp.groupby("IDADE_ANALISE")[list(COLS_NOTAS.keys())].mean().reset_index()
        )
        lng = pd.melt(
            desemp,
            id_vars="IDADE_ANALISE",
            value_vars=list(COLS_NOTAS.keys()),
            var_name="Prova",
            value_name="Nota Média",
        )
        lng["Prova"] = lng["Prova"].map(COLS_NOTAS)
        fig_linha = px.line(
            lng[lng["IDADE_ANALISE"] <= 65],
            x="IDADE_ANALISE",
            y="Nota Média",
            color="Prova",
            markers=True,
            color_discrete_sequence=PALETA,
        )
        fig_linha.update_traces(
            hovertemplate="Idade: <b>%{x}</b><br>Nota Média: <b>%{y:.1f}</b><extra></extra>"
        )
        fig_linha.update_layout(
            title="Desempenho por Idade dos Presentes",
            xaxis_title="Idade Estimada",
            yaxis_title="Nota Média",
            template="plotly_white",
        )
    return fig_hist, fig_linha


@app.callback(
    Output("tp-tri", "figure"),
    Output("tp-redacao", "figure"),
    Output("tp-participacao", "figure"),
    Input("ano-tp", "value"),
    Input("sexo-tp", "value"),
    Input("cert-tp", "value"),
    Input("areas-temporal", "value"),
)
def cb_tp(anos, sexos, certs, areas):
    db = fp(anos, sexos, certs, df_bruto)
    areas = areas or TODAS_AREAS
    db2 = db.dropna(subset=list(COLS_NOTAS.keys()), how="all")

    if db2.empty:
        return vazio(), vazio(), vazio()

    med = db2.groupby("NU_ANO")[list(COLS_NOTAS.keys())].mean().reset_index()
    lng = pd.melt(
        med,
        id_vars="NU_ANO",
        value_vars=list(COLS_NOTAS.keys()),
        var_name="Prova",
        value_name="Nota Média",
    )
    lng["Prova"] = lng["Prova"].map(COLS_NOTAS)
    lng["NU_ANO"] = lng["NU_ANO"].astype(str)

    # TRI
    df_tri = lng[(lng["Prova"] != "Redação") & (lng["Prova"].isin(areas))]
    if df_tri.empty:
        fig_tri = vazio()
    else:
        fig_tri = px.line(
            df_tri,
            x="NU_ANO",
            y="Nota Média",
            color="Prova",
            markers=True,
            text="Nota Média",
            color_discrete_sequence=[COR_AZUL, COR_LARANJA, COR_VERDE, COR_AMARELO],
            category_orders={"NU_ANO": [str(a) for a in ANOS_DISP]},
        )
        fig_tri.update_traces(
            textposition="top center",
            texttemplate="%{text:.1f}",
            hovertemplate="Ano: <b>%{x}</b><br>Nota: <b>%{y:.1f}</b><extra></extra>",
        )
        fig_tri.update_layout(
            title="Evolução das Notas Objetivas (TRI)",
            xaxis_title="Ano",
            yaxis_title="Nota Média",
            template="plotly_white",
            xaxis=dict(type="category"),
        )

    # Redação
    if "Redação" in areas:
        df_red = lng[lng["Prova"] == "Redação"]
        fig_red = px.line(
            df_red,
            x="NU_ANO",
            y="Nota Média",
            markers=True,
            text="Nota Média",
            color_discrete_sequence=[COR_LARANJA],
            category_orders={"NU_ANO": [str(a) for a in ANOS_DISP]},
        )
        fig_red.update_traces(
            name="Redação",
            showlegend=True,
            textposition="top center",
            texttemplate="%{text:.2f}",
            hovertemplate="Ano: <b>%{x}</b><br>Redação: <b>%{y:.2f}</b><extra></extra>",
        )
        fig_red.update_layout(
            title="Evolução da Nota de Redação",
            xaxis_title="Ano",
            yaxis_title="Nota (0–10)",
            template="plotly_white",
            yaxis=dict(range=[0, 10]),
            xaxis=dict(type="category"),
        )
    else:
        fig_red = vazio()

    # Taxa de participação
    cols_p = ["TP_PRESENCA_LC", "TP_PRESENCA_CH", "TP_PRESENCA_MT", "TP_PRESENCA_CN"]
    nomes_p = {
        "TP_PRESENCA_LC": "Linguagens",
        "TP_PRESENCA_CH": "Ciências Humanas",
        "TP_PRESENCA_MT": "Matemática",
        "TP_PRESENCA_CN": "Ciências da Natureza",
    }
    rows = []
    for ano in ANOS_DISP:
        da = db[db["NU_ANO"] == ano]
        for col in cols_p:
            val = da[col].notna()
            taxa = (
                (da.loc[val, col] == 1).sum() / val.sum() * 100 if val.sum() > 0 else 0
            )
            rows.append(
                {"Ano": str(ano), "Prova": nomes_p[col], "Taxa": round(taxa, 1)}
            )
    df_t = pd.DataFrame(rows)
    fig_part = px.bar(
        df_t,
        x="Prova",
        y="Taxa",
        color="Ano",
        barmode="group",
        text_auto=".1f",
        color_discrete_sequence=[COR_AZUL, COR_AZUL_C, COR_AMARELO],
    )
    fig_part.update_traces(
        hovertemplate="<b>%{x}</b> — %{fullData.name}<br>Presença: <b>%{y:.1f}%</b><extra></extra>"
    )
    fig_part.update_layout(
        title="Taxa de Participação por Área e Ano",
        xaxis_title="",
        yaxis_title="Candidatos Presentes (%)",
        template="plotly_white",
        yaxis=dict(range=[0, 50]),
    )
    return fig_tri, fig_red, fig_part

@app.callback(
    Output("se-renda", "figure"),
    Output("se-escolaridade", "figure"),
    Output("se-escola-box", "figure"),
    Input("ano-se", "value"),
    Input("sexo-se", "value"),
    Input("cert-se", "value"),
)
def cb_se(anos, sexos, certs):
    dp = fp(anos, sexos, certs, df_pres)
    db = fp(anos, sexos, certs, df_bruto)

    db["Q05_LABEL"] = db["Q05"].astype(str).str.strip().map(MAP_Q05)
    db["NOTA_GERAL"] = db[NOTAS_OBJ].mean(axis=1)
    df_r = (
        db[db["Q05_LABEL"].notna()]
        .groupby("Q05_LABEL")["NOTA_GERAL"]
        .mean()
        .reindex(ORDEM_RENDA)
        .reset_index()
    )
    df_r.columns = ["Renda Familiar", "Nota Média Geral"]

    fig_renda = px.bar(
        df_r,
        y="Renda Familiar",
        x="Nota Média Geral",
        orientation="h",
        text_auto=".1f",
        color="Nota Média Geral",
        color_continuous_scale=["#dbeafe", "#1d4ed8"],
    )
    fig_renda.update_traces(
        hovertemplate="<b>%{y}</b><br>Nota Média: <b>%{x:.1f}</b><extra></extra>"
    )
    fig_renda.update_layout(
        title="Renda Familiar (Q05) × Nota Média Geral",
        xaxis_title="Nota Média (TRI)",
        yaxis_title="",
        template="plotly_white",
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="array", categoryarray=ORDEM_RENDA),
        height=420,
    )

    dp["Q01_LABEL"] = dp["Q01"].astype(str).str.strip().map(MAP_Q01)
    df_e = (
        dp[dp["Q01_LABEL"].notna()]
        .groupby("Q01_LABEL")[NOTAS_OBJ]
        .mean()
        .reindex(ORDEM_ESC)
        .reset_index()
    )
    df_e.columns = ["Escolaridade da Mãe"] + NOMES_OBJ
    lng_e = pd.melt(
        df_e,
        id_vars="Escolaridade da Mãe",
        value_vars=NOMES_OBJ,
        var_name="Área",
        value_name="Nota Média",
    )

    fig_esc = px.line(
        lng_e,
        x="Escolaridade da Mãe",
        y="Nota Média",
        color="Área",
        markers=True,
        color_discrete_sequence=PALETA,
        category_orders={"Escolaridade da Mãe": ORDEM_ESC},
    )
    fig_esc.update_traces(
        hovertemplate="<b>%{x}</b><br>Nota Média: <b>%{y:.1f}</b><extra></extra>"
    )
    fig_esc.update_layout(
        title="Escolaridade da Mãe (Q01) × Desempenho por Área",
        xaxis_title="",
        yaxis_title="Nota Média (TRI)",
        template="plotly_white",
        height=380,
    )


    dp["Q06_LABEL"] = dp["Q06"].astype(str).str.strip().map(MAP_Q06)
    df_box = dp[dp["Q06_LABEL"].notna() & dp["NU_NOTA_REDACAO"].notna()]
    cores_box = [COR_AZUL_C, COR_LARANJA, COR_VERDE, COR_AMARELO]
    fig_box = go.Figure()
    for i, escola in enumerate(ORDEM_ESCOLA):
        vals = df_box.loc[df_box["Q06_LABEL"] == escola, "NU_NOTA_REDACAO"]
        fig_box.add_trace(
            go.Box(
                y=vals,
                name=escola,
                marker_color=cores_box[i],
                boxmean=True,
                hovertemplate=f"<b>{escola}</b><br>Nota: <b>%{{y:.2f}}</b><extra></extra>",
            )
        )
    fig_box.update_layout(
        title="Tipo de Escola Frequentada (Q06) × Nota de Redação",
        yaxis_title="Nota de Redação (0–10)",
        template="plotly_white",
        yaxis=dict(range=[0, 10]),
        showlegend=False,
        height=380,
    )
    return fig_renda, fig_esc, fig_box


if __name__ == "__main__":
    print("\n🚀 Acesse: http://127.0.0.1:8050")
    app.run(debug=True)
