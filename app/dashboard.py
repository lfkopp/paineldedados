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
            text="COPPEAD NUPEC",
            textangle=0,
            opacity=0.1,
            font=dict(color="black", size=20),
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
                            src = app.get_asset_url("gestao.png"),
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
                dcc.Tab(label='Página Inicial', value='tab-1'),
                dcc.Tab(label='Dados Socioeconômicos', value='tab-2'),
                dcc.Tab(label='Financeiro', value='tab-3'),
                dcc.Tab(label='Royalties', value='tab-4'),
                dcc.Tab(label='Desenvolvimento Sustentável', value='tab-5'),
                dcc.Tab(label='Saúde & COVID19', value='tab-6'),
                dcc.Tab(label='Outros links', value='tab-7'),
            ]),
            html.Div(id='tab-content')
        ]),
        html.Div([
                html.Div([
                        html.Div([
                                html.P("Desenvolvido por"),
                                html.A(html.Img(
                                        src = app.get_asset_url("catedra_nupec.png"),
                                        id = "catedra-image",
                                        style = {
                                            "height": "40px",
                                            "width": "auto",
                                            "margin-bottom": "-5px",
                                            "margin-right": "5px"
                                        }
                                    ),
                                    href = "http://paineldedados.herokuapp.com/")
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

pagina_inicial = html.Div([
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
html.H4(["Pesquisadores"]),
html.Div([
    html.Div([
        html.Img(
                src = app.get_asset_url("Ariane.jpg"),
                id = "ariane-image",
                title = 'Ariane Figueira',
                style = {
                    "align": "center",
                        "height": "120px",
                    "width": "auto",
                    "margin-bottom": "2px"
                },
            ),
        html.P(["Ariane Figueira"])],
        style = {
            'margin-bottom': '10px',
            'margin-left': '4px',
            'margin-right': '4px'
        }
    ),
    
        html.Div([
            html.Img(
                    src = app.get_asset_url("Eduardo_Raupp.jpg"),
                    id = "eduardo-image",
                    title = 'Eduardo Raupp',
                    style = {
                        "align": "center",
                        "height": "120px",
                        "width": "auto",
                        "margin-bottom": "2px"
                    },
                ),
            html.P(["Eduardo Raupp"])],
            style = {
                'margin-bottom': '10px',
                'margin-left': '4px',
                'margin-right': '4px'
        }
    ),
    
        html.Div([
            html.Img(
                    src = app.get_asset_url("Olavo-Diogo-150x150.jpg"),
                    id = "olavo-image",
                    title = 'Olavo Diogo',
                    style = {
                        "align": "center",
                        "height": "120px",
                        "width": "auto",
                        "margin-bottom": "2px"
                    },
                ),
            html.P(["Olavo Diogo"])],
            style = {
                'margin-bottom': '10px',
                'margin-left': '4px',
                'margin-right': '4px'
        }
    ),
            html.Div([
            html.Img(
                    src = app.get_asset_url("Marie_Anne.jpg"),
                    id = "marie-image",
                    title = 'Marie Anne Macadar',
                    style = {
                        "align": "center",
                        "height": "120px",
                        "width": "auto",
                        "margin-bottom": "2px"
                    },
                ),
            html.P(["Marie Anne Macadar"])],
            style = {
                'margin-bottom': '10px',
                'margin-left': '4px',
                'margin-right': '4px'
        }
    )

    ],className = "row container-display",
),

# html.H4(["Outros"]),
# html.Div([


#     html.Div([
#         html.Img(
#                 src = app.get_asset_url("Ariane.jpg"),
#                 id = "kopp-image",
#                 style = {
#                     "align": "center",
#                         "height": "120px",
#                     "width": "auto",
#                     "margin-bottom": "2px"
#                 },
#             ),
#         html.P(["Luis Filipe Kopp"])],
#         style = {
#             'margin-bottom': '10px',
#             'margin-left': '4px',
#             'margin-right': '4px'
#         }
#     ),

#         html.Div([
#         html.Img(
#                 src = app.get_asset_url("Ariane.jpg"),
#                 id = "helena-image",
#                 style = {
#                     "align": "center",
#                         "height": "120px",
#                     "width": "auto",
#                     "margin-bottom": "2px"
#                 },
#             ),
#         html.P(["Helena"])],
#         style = {
#             'margin-bottom': '10px',
#             'margin-left': '4px',
#             'margin-right': '4px'
#         }
#     ),

#         html.Div([
#         html.Img(
#                 src = app.get_asset_url("Ariane.jpg"),
#                 id = "vanessa-image",
#                 style = {
#                     "align": "center",
#                         "height": "120px",
#                     "width": "auto",
#                     "margin-bottom": "2px"
#                 },
#             ),
#         html.P(["Vanessa"])],
#         style = {
#             'margin-bottom': '10px',
#             'margin-left': '4px',
#             'margin-right': '4px'
#         }
#     ),    

#     html.Div([
#         html.Img(
#                 src = app.get_asset_url("Ariane.jpg"),
#                 id = "matheus-image",
#                 style = {
#                     "align": "center",
#                         "height": "120px",
#                     "width": "auto",
#                     "margin-bottom": "2px"
#                 },
#             ),
#         html.P(["Matheus"])],
#         style = {
#             'margin-bottom': '10px',
#             'margin-left': '4px',
#             'margin-right': '4px'
#         }
#     ),

#     ],className = "row container-display",
# ),

html.H3(["Contato"]),
html.P("Para entrar em contato, enviar email para xxxxxx.xxxx@xxxx.com.br")
])

dados_socioeconomicos = html.Div([
    html.Div([
            html.Div([

             dcc.Dropdown(
                    id = "filtro-local",
                    multi = True,
                    placeholder = "Filtre por município",
                    value = 'NUPEC',
                    options=[{'label':name, 'value':name} for name in MUNICIPIOS]+[{'label':'NUPEC', 'value':'NUPEC'}],
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
                    [dcc.Graph(className = "graph", id = 'my-graph1', figure = graf1('NUPEC')),
                        html.P("O Índice de Desenvolvimento Humano Municipal (IDHM) é uma medida composta de indicadores de três dimensões do desenvolvimento humano: longevidade, educação e renda. O índice varia de 0 a 1. Quanto mais próximo de 1, maior o desenvolvimento humano."),
                        html.P("Fonte: http://www.atlasbrasil.org.br/ranking")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph2', figure = graf2('NUPEC')),
                        html.P("O Índice de Gini é um instrumento para medir o grau de concentração de renda em determinado grupo. Ele aponta a diferença entre os rendimentos dos mais pobres e dos mais ricos. O valor zero representa a situação de igualdade, ou seja, todos têm a mesma renda. O valor um está no extremo oposto, isto é, uma só pessoa detém toda a riqueza."),
                        html.P("Fonte: http://tabnet.datasus.gov.br/cgi/ibge/censo/cnv/ginirj.def")
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
                    [dcc.Graph(className = "graph", id = 'my-graph3', figure = graf3('NUPEC')),
                        html.P("A população...."),
                        html.P("Fonte: https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html?=&t=downloads")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph4', figure = graf4('NUPEC')),
                        html.P("xx"),
                        html.P("Fonte: https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html?=&t=downloads")
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
                    [dcc.Graph(className = "graph", id = 'my-graph5', figure = graf5('NUPEC')),
                        html.P("A população...."),
                        html.P("Fonte: https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html?=&t=downloads")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                ),
                html.Div(
                    [dcc.Graph(className = "graph", id = 'my-graph6', figure = graf5('NUPEC')),
                        html.P("xx"),
                        html.P("Fonte: xx")
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
])



financeiro = html.Div([
    html.Div([
                            html.Div([
                            dcc.Dropdown(
                                    id = "filtro-local-fin",
                                    multi = True,
                                    placeholder = "Filtre por município",
                                    value = NUPEC,
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS],
                                    style = {
                                        'width': '100%',
                                        'margin-left': '10px',
                                        'margin-right': '10px',
                                        'z-index':10
                                    },
                                    disabled = False
                                )
                            ], id = 'filtros3', className = 'row flex-display', style = {
                                'margin-top': '3px'
                            })
                        ],
                        className = 'pretty_container sticky',
                        id = 'filtros',
                        style = {
                            'text-align': 'left'
                    }
                        ),
   
      html.Div(  ##graficos
            [       
            html.Div([  ## primeira linha
               
                    html.Div([  ## grafico 1
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-fin-1', figure = graf_fin_1(NUPEC)),

                                                     html.Div([        ### dropddown
                                dcc.Dropdown(
                                        id = "filtro-funcao-fin",
                                        multi = False,
                                        placeholder = "Filtre por funcao",
                                        value = 'Despesas Exceto Intraorçamentárias',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in financeiros],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '10px',
                                            'margin-right': '10px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    )
                                ], id = 'filtros4', className = 'row flex-display', style = {
                                    'margin-top': '3px'
                        }),

                                            html.P("xxxx"),
                                            html.P("Fonte: xxx")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '50%',
                                            'margin': '5px'
                                        }
                                    ),
                
                html.Div([   ## grafico 2
                     
                     dcc.Graph(className = "graph", id = 'my-graph-fin-2', figure = graf_fin_2(NUPEC)),

                     html.Div([      ### dropddown
                                dcc.Dropdown(
                                        id = "filtro-funcao1-fin",
                                        multi = False,
                                        placeholder = "Filtre por funcao",
                                        value = '10 - Saúde',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in financeiros],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '10px',
                                            'margin-right': '10px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    ),
                                dcc.Dropdown(
                                        id = "filtro-funcao2-fin",
                                        multi = False,
                                        placeholder = "Filtre por funcao",
                                        value = '12 - Educação',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in financeiros],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '10px',
                                            'margin-right': '10px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    )
                                ], id = 'filtros6', className = 'row flex-display', style = {
                                    'margin-top': '3px'
                        }),

                        html.P("xxxx"),
                        html.P("Fonte: xxx")
                    ],
                    className = "pretty_container", style = {
                        'width': '50%',
                        'margin': '5px'
                    }
                )
                
                ],
            className = "row container-display",
            style = {
                'margin-bottom': '10px',
                'margin-left': '-4px',
                'margin-right': '-4px'
            }
        ),
      
])

])

royalties = html.Div([
    html.Div([
                            html.Div([
                            dcc.Dropdown(
                                    id = "filtro-local-roy",
                                    multi = True,
                                    placeholder = "Filtre por município",
                                    value = NUPEC,
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS],
                                    style = {
                                        'width': '100%',
                                        'margin-left': '10px',
                                        'margin-right': '10px',
                                        'z-index':10
                                    },
                                    disabled = False
                                )
                            ], id = 'filtros3', className = 'row flex-display', style = {
                                'margin-top': '3px'
                            })
                        ],
                        className = 'pretty_container sticky',
                        id = 'filtros',
                        style = {
                            'text-align': 'left'
                    }
                        ),
   
      html.Div(  ##graficos
            [       
            html.Div([  ## primeira linha
               
                    html.Div([  ## grafico 1
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-roy-1', figure = graf_roy_1(NUPEC)),

  
                                            html.P("xxxx"),
                                            html.P("Fonte: xxx")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '50%',
                                            'margin': '5px'
                                        }
                                    ),

                                                    html.Div([  ## grafico 2
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-roy-2', figure = graf_roy_2(NUPEC)),

  
                                            html.P("xxxx"),
                                            html.P("Fonte: xxx")
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
      
])

])

ods = html.Div([
    html.Div([
                            html.Div([
                            dcc.Dropdown(
                                    id = "filtro-local-ods",
                                    multi = True,
                                    placeholder = "Filtre por município",
                                    value = NUPEC,
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS],
                                    style = {
                                        'width': '100%',
                                        'margin-left': '10px',
                                        'margin-right': '10px',
                                        'z-index':10
                                    },
                                    disabled = False
                                )
                            ], id = 'filtros_ods', className = 'row flex-display', style = {
                                'margin-top': '3px'
                            })
                        ],
                        className = 'pretty_container sticky',
                        id = 'filtros',
                        style = {
                            'text-align': 'left'
                    }
                        ),
   
      html.Div(  ##graficos
            [       
            html.Div([  ## primeira linha
               
                    html.Div([  ## grafico 1
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-ods-1', figure = graf_ods_1(NUPEC)),

  
                                            html.P("xxxx"), 
                                            html.P("Fonte: xxx")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '50%',
                                            'margin': '5px'
                                        }
                                    ),

                                                    html.Div([  ## grafico 2
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-ods-2', figure = graf_ods_2(NUPEC)),

  
                                            html.P("xxxx"),
                                            html.P("Fonte: xxx")
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
      
])

])

saude = html.Div([
    html.Div([
                            html.Div([
                            dcc.Dropdown(
                                    id = "filtro-local-saude",
                                    multi = True,
                                    placeholder = "Filtre por município",
                                    value = NUPEC,
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS],
                                    style = {
                                        'width': '100%',
                                        'margin-left': '10px',
                                        'margin-right': '10px',
                                        'z-index':10
                                    },
                                    disabled = False
                                )
                            ], id = 'filtros_ods', className = 'row flex-display', style = {
                                'margin-top': '3px'
                            })
                        ],
                        className = 'pretty_container sticky',
                        id = 'filtros',
                        style = {
                            'text-align': 'left'
                    }
                        ),
   
      html.Div(  ##graficos
            [       
            html.Div([  ## primeira linha
               
                    html.Div([  ## grafico 1
       
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-saude-1', figure = graf_saude_1(NUPEC)),

  
                                            html.P("xxxx"), 
                                            html.P("Fonte: xxx")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '50%',
                                            'margin': '5px'
                                        }
                                    ),

                                                    html.Div([  ## grafico 2
                 
                                     dcc.Dropdown( 
                                        id = "filtro-funcao-saude",
                                        multi = False,
                                        placeholder = "Filtre por funcao",
                                        value = 'obitopor100k',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in saudes],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '-4px',
                                            'margin-right': '-4px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    ),
                                    dcc.Graph(className = "graph", id = 'my-graph-saude-2', figure = graf_saude_2(NUPEC)),

  
                                            html.P("xxxx"),
                                            html.P("Fonte: xxx")
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
      
])

])

outros_links = html.Div([html.H3(["Outros links"]),

html.Div(outroslinks(html,app))


])

# index layout
app.layout = base

# "complete" layout
app.validation_layout = html.Div([
    base,
    pagina_inicial,
    dados_socioeconomicos, 
    financeiro, 
    royalties,
    ods,
    saude,
    outros_links
])

# Callbacks

@app.callback(Output('tab-content', 'children'),[Input('tab', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return pagina_inicial
    elif tab == 'tab-2':
        return dados_socioeconomicos
    elif tab == 'tab-3':
        return financeiro
    elif tab == 'tab-4':
        return royalties
    elif tab == 'tab-5':
        return ods
    elif tab == 'tab-6':
        return saude
    elif tab == 'tab-7':
        return outros_links

@app.callback([Output('my-graph1','figure'),Output('my-graph2','figure'),Output('my-graph3','figure'),Output('my-graph4','figure'),Output('my-graph5','figure'),Output('my-graph6','figure')],[Input('filtro-local','value')])
def update_graph1(local):
    return graf1(local), graf2(local), graf3(local), graf4(local), graf5(local), graf5(local)


@app.callback(Output('my-graph-fin-1','figure'),[Input('filtro-local-fin','value'),Input('filtro-funcao-fin','value')])
def update_graph_fin_1(local,funcao):
    return graf_fin_1(local,funcao)

@app.callback(Output('my-graph-fin-2','figure'),[Input('filtro-local-fin','value'),Input('filtro-funcao1-fin','value'),Input('filtro-funcao2-fin','value')])
def update_graph_fin_2(local,funcao1,funcao2):
    return graf_fin_2(local,funcao1,funcao2)

@app.callback(Output('my-graph-roy-1','figure'),[Input('filtro-local-roy','value')])
def update_graph_roy_1(local):
    return graf_roy_1(local)

@app.callback(Output('my-graph-roy-2','figure'),[Input('filtro-local-roy','value')])
def update_graph_roy_2(local):
    return graf_roy_2(local)

@app.callback([Output('my-graph-ods-1','figure'),Output('my-graph-ods-2','figure')],[Input('filtro-local-ods','value')])
def update_graph_ods_1(local):
    return graf_ods_1(local),graf_ods_2(local)

@app.callback(Output('my-graph-saude-1','figure'),[Input('filtro-local-saude','value'),Input('filtro-funcao-saude','value')])
def update_graph_saude_1(local,funcao):
    return graf_saude_1(local)

@app.callback(Output('my-graph-saude-2','figure'),[Input('filtro-local-saude','value'),Input('filtro-funcao-saude','value')])
def update_graph_saude_2(local,funcao):
    return  graf_saude_2(local,funcao) 