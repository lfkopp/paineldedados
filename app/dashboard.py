# Imports
from app.config import app
from app.functions import *
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

# Graph template
pio.templates["covid"] = go.layout.Template(
    layout_annotations=[
        dict(
            name="ufrj",
            text="UFRJ",
            textangle=0,
            opacity=0.1,
            font=dict(color="black", size=100),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    ]
)
pio.templates.default = "plotly+covid"

# App layout

base = html.Div([
    html.Div(children = [
        html.Div(children = [
                html.Div([
                        html.Img(
                            src = app.get_asset_url("observatorio.png"),
                            id = "logo-image",
                            style = {
                                "height": "80px",
                                "width": "auto",
                                "margin-bottom": "3px",
                            },
                        )
                    ],
                    className = 'one-half column',
                    style = {
                        'text-align': 'left',
                        'margin-left': '2px',
                        'width': '100%'
                    }),
                html.Div(className = 'one-third column'),
                html.Div([
                        html.A(html.Img(
                            src = app.get_asset_url("catedra_nupec.png"),
                            id = "nupec-image",
                            style = {
                                "height": "75px",
                                "width": "auto",
                                "margin-bottom": "15px",
                                "margin-left": "15px",
                            },
                        ),href="https://www.nupec.org/", target="_blank"),
                        html.A(html.Img(
                            src = app.get_asset_url("minerva.jpg"),
                            id = "minerva-image",
                            style = {
                                "height": "75px",
                                "width": "auto",
                                "margin-bottom": "15px",
                                "margin-left": "15px",
                            },
                        ),href="https://ufrj.br",target="_blank"),
                    ],
                    className = 'one-half column',
                    style = {
                        'text-align': 'right',
                        'width': '101%'
                    })
            ],
            id = "header",
            className = "row flex-display",
            style = {
                "margin-bottom": "10px",
                'margin-top': '-40px'
            },
        ),
        html.Div([
            dcc.Tabs(id='tab', value='tab-1', children=[
                dcc.Tab(label='Informações Básicas', value='tab-1'),
                dcc.Tab(label='Painel de Controle', value='tab-2'),
            ]),
            html.Div(id='tab-content')
        ]),
        html.Div([
                html.Div([
                        html.Div([
                                html.P("Desenvolvido por"),
                                html.A(html.Img(
                                        src = app.get_asset_url("labnet.jpeg"),
                                        id = "labnet-image",
                                        style = {
                                            "height": "40px",
                                            "width": "auto",
                                            "margin-bottom": "-5px",
                                            "margin-right": "5px"
                                        }
                                    ),
                                    href = "http://labnet.nce.ufrj.br/")
                            ],
                            className = "one-half column",
                            style = {
                                'text-align': 'left'
                            }
                        ),
                        html.Div(className = "one-half column"),
                        html.Div(className = "one-half column",
                            children = [
                                html.P("Apoio"),
                                html.Img(
                                    src = app.get_asset_url("logo_coppead_top-126x40.png"),
                                    id = "nce-image",
                                    style = {
                                        "height": "35px",
                                        "width": "auto",
                                        "margin-bottom": "10px"
                                    },
                                )
                            ],
                            style = {
                                'text-align': 'right'
                            }
                        )
                    ],
                    id = "footer",
                    className = "row flex-display"
                ),
                html.Div(className = "row",
                    children = [
                        html.P("Contato: kopp@labnet.nce.ufrj.br")
                    ],
                    style = {
                        'text-align': 'left',
                        'margin-bottom': '-10px'
                    }
                )
            ],
            style = {
                'margin-top': '18px'
            })
    ])
])

# Tabs

covidimetro = html.Div([
html.H3(["Cátedra NUPEC"]),
html.Div([
        
        html.P(["""Criada com os principais objetivos de: 
            fomentar o ensino e a pesquisa sobre gestão local; estimular
            a criação de um centro de estudos sobre governo local no 
            âmbito de uma Escola de Negócios promovendo a interação 
            público-privada como estratégia de desenvolvimento; inspirar 
            a inovação na gestão pública local aproximando os gestores 
            públicos, privados e os cidadãos; gerar e disseminar 
            conhecimento de vanguarda sobre a gestão local que permita 
            ações de impacto social; e promover a formação de lideranças 
            acadêmicas e executivas voltadas para a modernização da 
            gestão local."""
            ])

    ],
    className = "row container-display",
    style = {
        'margin-bottom': '10px',
        'margin-left': '4px',
        'margin-right': '4px'
    }
),

html.H3(["Equipe"]),
html.Div([
    html.Div([
        html.Img(
                src = app.get_asset_url("Ariane.jpg"),
                id = "ariane-image",
                style = {
                    "align": "center",
                        "height": "120px",
                    "width": "auto",
                    "margin-bottom": "2px"
                },
            ),
        html.P(["Ariane"])

        ],

        style = {
            'margin-bottom': '10px',
            'margin-left': '4px',
            'margin-right': '4px'
        }
    ),
    
        html.Div([
            html.Img(
                    src = app.get_asset_url("Eduardo_Raupp.jpg"),
                    id = "ariane-image",
                    style = {
                        "align": "center",
                        "height": "120px",
                        "width": "auto",
                        "margin-bottom": "2px"
                    },
                ),
            html.P(["Eduardo Raupp"])

            ],
            style = {
                'margin-bottom': '10px',
                'margin-left': '4px',
                'margin-right': '4px'
        }
    ),

            html.Div([
            html.Img(
                    src = app.get_asset_url("Marie_Anne.jpg"),
                    id = "ariane-image",
                    style = {
                        "align": "center",
                        "height": "120px",
                        "width": "auto",
                        "margin-bottom": "2px"
                    },
                ),
            html.P(["Marie Anne"])

            ],
            style = {
                'margin-bottom': '10px',
                'margin-left': '4px',
                'margin-right': '4px'
        }
    )

    ],className = "row container-display",
)])

geral = html.Div([
    html.Div([
            html.Div([

             dcc.Dropdown(
                    id = "filtro-local",
                    multi = True,
                    placeholder = "Filtre por município",
                    value = [],
                    style = {
                        'width': '100%',
                        'margin-left': '10px',
                        'margin-right': '10px'
                    },
                    disabled = False
                )
            ], id = 'filtros2', className = 'row flex-display', style = {
                'margin-top': '3px'
            })
        ],
        className = 'pretty_container sticky',
        id = 'filtros',
        style = {
            'text-align': 'left'
    }
        ),
   
      html.Div(
            [
                html.Div(
                    [html.H3("titulo xxx"),
                    dcc.Graph(className = "graph", id = 'my-graph3', figure = graf3()),
                        html.P("O Índice de Desenvolvimento Humano Municipal (IDHM) é uma medida composta de indicadores de três dimensões do desenvolvimento humano: longevidade, educação e renda. O índice varia de 0 a 1. Quanto mais próximo de 1, maior o desenvolvimento humano."),
                        html.P("Fonte: xxxx")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph4', figure = graf4()),
                        html.P("O Índice de Gini é um instrumento para medir o grau de concentração de renda em determinado grupo. Ele aponta a diferença entre os rendimentos dos mais pobres e dos mais ricos. O valor zero representa a situação de igualdade, ou seja, todos têm a mesma renda. O valor um está no extremo oposto, isto é, uma só pessoa detém toda a riqueza."),
                        html.P("Na prática, o Índice de Gini costuma comparar os 20% mais pobres com os 20% mais ricos. No Relatório de Desenvolvimento Humano 2004, elaborado pelo Pnud, o Brasil aparece com Índice de 0,591, quase no final da lista de 127 países. Apenas sete nações apresentam maior concentração de renda."),
                        html.P("Fonte: xxxx")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
            ],
            className = "row container-display",
            style = {
                'margin-bottom': '10px',
                'margin-left': '-4px',
                'margin-right': '-4px'
            }
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph1', figure = scatter1(dados_covid)),
                        html.P("Evolução do número de casos ao longo do tempo, comparando o acumulado total e novas ocorrências a cada dia. *Filtros aplicáveis.")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph2', figure = graf2(dados_covid)),
                        html.P("Comparação da evolução no número de casos entre os municípios do Estado do Rio de Janeiro, em escala logarítmica pelo tempo. Apenas municípios com mais de 1000 casos notificados, independente da classificação.")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
            ],
            className = "row container-display",
            style = {
                'margin-bottom': '10px',
                'margin-left': '-4px',
                'margin-right': '-4px' 
            }
        ),
   
        html.Div(
            [
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph5', figure = graf5(dados_covid)),
                        html.P("Distribuição de casos notificados por idade. Verifica-se maior ocorrência na faixa etária dos 20 aos 60 anos, com maior predominância de casos entre mulheres. *Filtros aplicáveis.")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph6', figure = graf6(dados_covid)),
                        html.P("Distribuição de casos confirmados com óbito por idade.")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
            ],
            className = "row container-display",
            style = {
                'margin-bottom': '10px',
                'margin-left': '-4px',
                'margin-right': '-4px'
            }
        )
])

# index layout
app.layout = base

# "complete" layout
app.validation_layout = html.Div([
    base,
    covidimetro,
    geral
])

# Callbacks

@app.callback(Output('tab-content', 'children'),
              [Input('tab', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return covidimetro
    elif tab == 'tab-2':
        return geral

@app.callback(
    [Output("filtro-local","options"),
    Output("filtro-local","disabled")],
    [Input("filtro-uf","value")]
)
def define_municipio(uf):
    if len(uf) != 0:
        df = dados_covid.loc[dados_covid['estado'].isin(uf)]
        municipios = []
        numMunicipios = len(RJ_MUN_GEOJSON["features"])
        for i in range(numMunicipios):
            municipios.append(RJ_MUN_GEOJSON["features"][i]["properties"]["name"])
        options=[
            {"label": str(cidade),"value": str((unidecode.unidecode(cidade)).upper())}
            for cidade in municipios
        ]
        disab = False
    else:
        options = []
        disab = True
    return options,disab

@app.callback(
    [Output("total_confirmados","children"),
    Output("total_obitos","children")],
    [Input("filtro-sexo","value")]
)
def update_info(sex,age,local,classificacao,data1,data2,uf):
    df = filtra_info(dados_covid,sex,age,local,classificacao,data1,data2,uf)
    age.sort()
    localidade_uf = "RJ"
    if len(local) != 0:
        localidade_mun = ", ".join(local)
        if len(local) == 1:
            localidade_mun = local[:]
    else:
        localidade_mun = "Todos os municípios"
    if len(sex) != 0:
        sexo = ", ".join(sex)
    else:
        sexo = "-"
    if len(age) != 0:
        idade = str(int(age[0][0:2]))+" a "+str(int(age[-1][-2:]))
        if age[-1] == '6060':
            idade = str(int(age[0][0:2]))+" a 60+"
    else:
        idade = "-"
    resumo_c = len(df.loc[df['classificacaoFinal'] == 'CONFIRMADO'].index)
    resumo_o = len(df.loc[(df['evolucaoCaso'] == 'OBITO') & (df['classificacaoFinal'] == 'CONFIRMADO')].index)
    resumo_r = len(df.loc[df['evolucaoCaso'] == 'RECUPERADO'].index)
    resumo_l = "{:.2f} %".format((len(df.loc[(df['evolucaoCaso'] == 'OBITO') & (df['classificacaoFinal'] == 'CONFIRMADO')].index)/len(df.loc[df['classificacaoFinal'] == 'CONFIRMADO'].index))*100).replace('.',',')
    return (resumo_c,resumo_o)

@app.callback(
    [Output("my-graph5","figure")],
    [Input("filtro-local","value"),
    Input("filtro-classificacao","value"),
    Input("filtro-data","date"),
    Input("filtro-data2","date")]
)
def update_graphs(local,classificacao,data1,data2):
    df = filtra_graph(dados_covid,local,classificacao,data1,data2)
    return [graf5(df)]

@app.callback(
    Output('my-graph1','figure'),
    [Input('filtro-local','value')])

def update_scatter1(idade,sexo,uf,mun):
    df = filtra_scatter(dados_covid,mun)
    return scatter1(df)


