# Imports
from app.config import app
from app.functions import *
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq


# Graph template
pio.templates["nupec"] = go.layout.Template(
    layout_annotations=[dict(name="ufrj",text="COPPEAD NUPEC",textangle=0,opacity=0.1,
                        font=dict(color="black", size=20),
                        xref="paper",yref="paper",x=0.5,y=0.5,showarrow=False)])

pio.templates.default = "plotly+nupec"

# App layout

base = html.Div([
    html.Div( [
        html.Div( [
            html.Div([html.Img(src = app.get_asset_url("painelgestao.png"),id = "logo-image",style = {"height": "100px","width": "auto","margin-bottom": "3px",},)],className = 'one-half column',style = {'text-align': 'left','margin-left': '2px','width':'100%',}),
            html.Div(className = 'one-third column'),
            html.Div([
                html.A(html.Img(src = app.get_asset_url("catedra_nupec.png"),id = "nupec-image",style = {"height": "75px","width": "auto","margin-bottom": "15px","margin-left": "15px",},),href="https://www.nupec.org/", target="_blank"),
                html.A(html.Img(src = app.get_asset_url("logo_coppead_top.png"),id = "coppead-image",style = {"height": "55px","width": "auto","margin-bottom": "15px","margin-left": "15px",},),href="https://coppead.ufrj.br",target="_blank"),
                html.A(html.Img(src = app.get_asset_url("minerva_watermark.jpg"),id = "minerva-image",style = {"height": "75px","width": "auto","margin-bottom": "15px","margin-left": "15px",},),href="https://ufrj.br",target="_blank"),
                ],className = 'one-half column',style = {'text-align': 'right','width': '100%'})
            ], id = "header",className = "row flex-display",style = {"margin-bottom": "10px",'margin-top': '-40px'},),
        html.Div([
            dcc.Tabs(id='tab', value='tab-1', children=[
                dcc.Tab(label='Página Inicial', value='tab-1'),
                dcc.Tab(label='Dados Socioeconômicos', value='tab-2'),
                dcc.Tab(label='Financeiro', value='tab-3'),
                dcc.Tab(label='Royalties', value='tab-4'),
                dcc.Tab(label='Desenvolvimento Sustentável', value='tab-5'),
                dcc.Tab(label='Saúde & COVID19', value='tab-6'),
                dcc.Tab(label='Outros links', value='tab-7'),],style={'height':'80px'}),
        html.Div(id='tab-content')
        ]),
    ],style={'max-width':'1600px','align':'center','margin':'auto'})
])

# Tabs

pagina_inicial = html.Div([
html.H3(["Cátedra NUPEC"]),
html.Div([
        html.P([
            """Uma Cátedra de Pesquisa consiste no financiamento, via doação por empresas, de atividades de ensino e  pesquisa. 
               O financiamento envolve recursos para um  professor responsável, assistentes de pesquisa, material didático, viagens,  
               suporte informático e apoio administrativo geral. Os objetivos de uma são a realização de pesquisas na área  específica 
               da Cátedra e o oferecimento de disciplinas dentro desta mesma área  de interesse, com o objetivo de formação de pessoal 
               com qualificação  especializada.""",
            html.H4("A Cátedra COPPEAD-NUPEC foi criada com os objetivos de:"),
            html.Ul([
                html.Li(['fomentar o ensino e a pesquisa sobre gestão local;']),
                html.Li(['estimular a criação de um centro de estudos sobre governo local no âmbito de uma Escola de Negócios promovendo a interação público-privada como estratégia de desenvolvimento;']),
                html.Li(['inspirar a inovação na gestão pública local aproximando os gestores públicos, privados e os cidadãos;']),
                html.Li(['gerar e disseminar conhecimento de vanguarda sobre a gestão local que permita ações de impacto social;']),
                html.Li(['promover a formação de lideranças acadêmicas e executivas voltadas para a modernização da gestão local.']),
                ], style={'margin-left':'10px'}),
            html.H4("As atividades propostas são:"),
            html.Ul([
                html.Li(['Monitoramento das Receitas e Despesas;']),
                html.Li(['Análise da Autonomia Orçamentária e Financeira;']),
                html.Li(['Acompanhamento da Gestão Fiscal e Tributária;']),
                html.Li(['Estudos sobre Novas Fontes de Recursos;']),
                html.Li(['O papel dos Royalties e Participações Especiais;']),
                html.Li(['Cenários Prospectivos de Fontes Alternativas de Receitas']),
                ], style={'margin-left':'10px'}),
            ])], className = "row container-display",style = {'margin': '20px'}),



#### INICIO EQUIPE ########
html.H3(["Equipe"]),
html.Div([
        html.Div([
        html.H4(["Pesquisadores"]),
        html.Div(fotos_prof(app,html),className = "row container-display"),
        ]),
        html.Div([
        html.H4(["Assistentes de Pesquisa"]),
        html.Div(fotos_assist(app,html),className = "row container-display")
        ])
    ], style = {'display': 'flex','flex-wrap': 'wrap', 'justify-content':'space-evenly','margin': '20px'}),
##### FIM EQUIPE ####

html.H3(["Contato"]),
html.P("Para entrar em contato, enviar email para painelgestaolocal@coppead.ufrj.br")
], style={'padding': '20px','background-color':'#fff','border':'1px solid lightgrey'})

##### FIM PAGINA INICIAL ####

dados_socioeconomicos = html.Div([
    html.Div([
            html.Div([
            html.P('Locais'),
            dcc.Dropdown(
                    id = "filtro-local",
                    multi = True,
                    placeholder = "Filtre por município",
                    value = 'NUPEC',
                    options=[{'label':name, 'value':name} for name in MUNICIPIOS]+[{'label':'NUPEC', 'value':'NUPEC'},{'label':'NORTE', 'value':'NORTE'},{'label':'CENTRO', 'value':'CENTRO'}],
                    style = {'width': '50%','margin-left': '10px','margin-right': '10px'},
                    disabled = False),
            html.P('Indicador'),
            dcc.Dropdown(
                    id = "filtro-funcao-soc",
                    multi = False,
                    placeholder = "Filtre por indicador",
                    value = 'GINI',
                    clearable=False,
                    options=[{'label':opt_soc[x]['label'], 'value':opt_soc[x]['name']} for x in opt_soc.keys()],
                    style = {
                        'width': '50%',
                        'margin-left': '10px',
                        'margin-right': '10px',
                        'z-index':15
                    },
                    disabled = False
                ),
            ], id = 'filtros2', className = 'row flex-display', style = {'margin-top': '3px'})
        ],className = 'pretty_container sticky',id = 'filtros',style = {'text-align': 'left'}),
   
      html.Div(
            [   html.Div(
                    [
                        dcc.Graph(className = "graph", id = 'my-graph-soc', figure = graf_soc(local='NUPEC',funcao='GINI')),
                   
                    html.P("Os indicadores dos municípios do RJ auxiliam a identificar a evolução social e econômica ao longo dos anos."),
                    html.P("IDHM e Gini ajudam a perceber o desenvolvimento e o grau de desigualdade."),
                    html.P("A Nota IDEB é um indicador da qualidade da educação."),
                    html.P("Em royalties, é possível avaliar o volume de recursos extra recebidos."),
                    html.P("População e densidade populacional servem para indicar os municípios populosos."),
                    
                     ],className = "pretty_container",style={'width':'100%', 'margin-bottom':'10'}),
            ],className = "row container-display", style={'flex-wrap': 'wrap', 'align-items': 'stretch'})])


financeiro = html.Div([
    html.Div([
                            html.Div([
                            dcc.Dropdown(
                                    id = "filtro-local-fin",
                                    multi = True,
                                    placeholder = "Filtre por município",
                                    value = 'NUPEC',
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS]+[{'label':'NUPEC', 'value':'NUPEC'},{'label':'NORTE', 'value':'NORTE'},{'label':'CENTRO', 'value':'CENTRO'}],
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
                            'text-align': 'left',
                            'height': '100%',
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

                                            html.P("Despesas ao longo dos anos, dividido por Função, de gasto."),
                                            html.P("Fonte: SICONFI (https://siconfi.tesouro.gov.br/)")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
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

                        html.P("Despesas comparadas por função. Indica o quanto uma despesa varia em relação a outra função. Por exemplo, a despesa com Educação tem crescido mais do que Saúde?"),
                        html.P("Fonte: SICONFI (https://siconfi.tesouro.gov.br/)")
                    ],
                    className = "pretty_container", style = {
                        'width': '100%',
                        'margin': '5px'
                    }
                ),

                                html.Div([   ## grafico 3
                     
                     dcc.Graph(className = "graph", id = 'my-graph-fin-3', figure = graf_fin_3(NUPEC)),

                     html.Div([      ### dropddown
                                dcc.Dropdown(
                                        id = "filtro-funcao1B-fin",
                                        multi = False,
                                        placeholder = "Filtre por funcao",
                                        value = 'total',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in eficiencias],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '10px',
                                            'margin-right': '10px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    ),
                                dcc.Dropdown(
                                        id = "filtro-funcao2B-fin",
                                        multi = False,
                                        placeholder = "Filtre por funcao",
                                        value = 'Despesas Correntes',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in eficiencias],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '10px',
                                            'margin-right': '10px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    )
                                ], id = 'filtros6b', className = 'row flex-display', style = {
                                    'margin-top': '3px'
                        }),

                        html.P("Comparação de despesas por tipo (despesas de investimento e despesas correntes). Dentro de despesas Correntes, o quanto é relativo a gasto com Pessoal? Municípios que recebem mais Royalties investem mais?"),
                        html.P("Fonte: SICONFI (https://siconfi.tesouro.gov.br/)")
                                         ],
                    className = "pretty_container", style = {
                        'width': '100%',
                        'margin': '5px'
                    }
                ),



                
                ],
            className = "row container-display",  
            style={'flex-wrap': 'wrap', 'align-items': 'stretch', 'margin':'0px -4px'}
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
                                    value = 'NUPEC',
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS]+[{'label':'NUPEC', 'value':'NUPEC'},{'label':'NORTE', 'value':'NORTE'},{'label':'CENTRO', 'value':'CENTRO'}],
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

  
                                            html.P("Total de receitas oriundas dos Royalties."),
                                             html.P("Fonte: SICONFI (https://siconfi.tesouro.gov.br/), ANP (https://www.gov.br/anp/pt-br/assuntos/royalties-e-outras-participacoes/royalties)")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
                                            'margin': '5px'
                                        }
                                    ),

                html.Div([  ## grafico 2
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-roy-2', figure = graf_roy_2(NUPEC)),

  
                                            html.P("Total de receita de Royalties normalizado pela população do município."),
                                            html.P("Fonte: SICONFI (https://siconfi.tesouro.gov.br/), ANP (https://www.gov.br/anp/pt-br/assuntos/royalties-e-outras-participacoes/royalties)")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
                                            'margin': '5px'
                                        }
                                    ),
                                html.Div([  ## grafico 3
                      dcc.Dropdown( 
                                        id = "filtro-detalhe-roy",
                                        multi = False,
                                        placeholder = "Filtre por tipo",
                                        value = 'Total Geral',
                                        clearable=False,
                                        options=[{'label':name, 'value':name} for name in detalhes_roy],
                                        style = {
                                            'width': '100%',
                                            'margin-left': '-4px',
                                            'margin-right': '-4px',
                                            'z-index':15
                                        },
                                        disabled = False
                                    ),
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-roy-3', figure = graf_roy_3(NUPEC)),

  



html.P("Fonte:"),
html.P("Secr.de Fazenda do Rio de Janeiro (TesouroRJ); TesouroNacionalTransparentes; ANP; SICONFI"),
html.P("(1)  Inclui os Royalties que são repassados de forma indireta, ou seja : (a) os Royalties que são repassados pela ANP aos Estado e posteriormente aos Municipios que são transferidos  todos os municipios considerando a população geral ate mesmo para municipios que nao recebem royalties da ANP e (b) e Fundo Especial do Petróleo – FEP"),
html.P("(2) Os dados das Transferencias da ANP e Participação Especial são os informados  pelo TesouroNacional"),
html.P("(3) O valor da Cessão Onerosa, estabelecida pela Lei nº 13.885/2019 , foi transferida  para as contas do FPM e não para as contas de Royalties para a grande parte dos municipios em 31/12/2019, segundo relatórios de contas do TCE-RJ."),
html.P("(4) Os Royalties - CFM e Royalties - CFH, são referentes as Compensações Financeiras de Recursos Minerais e Hidricos."),


html.P("links das fontes:"),
html.P("http://www.fazenda.rj.gov.br/tesouro/faces/oracle/webcenter/portalapp/pages/paginaDocumentos.jspx?datasource=UCMServer%23dDocName%3AWCC193245&_afrLoop=94961653942287012&_afrWindowMode=0&_afrWindowId=null&_adf.ctrl-state=5u1d99lfl_1#!%40%40%3F_afrWindowId%3Dnull%26_afrLoop%3D94961653942287012%26datasource%3DUCMServer%2523dDocName%253AWCC193245%26_afrWindowMode%3D0%26_adf.ctrl-state%3D5u1d99lfl_5"),
html.P("https://www.tesourotransparente.gov.br/temas/estados-e-municipios/transferencias-a-estados-e-municipios#:~:text=05%2F08%2F2021-,Parcela%20das%20receitas%20federais%20arrecadadas%20pela%20Uni%C3%A3o%20%C3%A9%20repassada%20aos,equil%C3%ADbrio%20s%C3%B3cio%2Decon%C3%B4mico%20entre%20Estados."),
html.P("https://www.gov.br/anp/pt-br/assuntos/royalties-e-outras-participacoes/royalties"),
html.P("https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_finbra/finbra_list.jsf"),
html.P("https://www.gov.br/economia/pt-br/assuntos/noticias/2019/12/governo-realiza-transferencia-de-r-11-73-bilhoes-da-cessao-onerosa-para-estados-e-municipios"),

html.P("""Achados:
(1) Analisando em detalhes as transferencias de Royalties dos Estado aos municipios, descobri que existe um erro no mês de fevereiro de 2018 nos dados disponiveis no site da Secretaria da Fazenda do RJ,  os valaores do referido mês estão dobrados. Após o acerto os dados conferem completamente com os informados como recebidos pelos municipios no Siconf.
(2) Essa coleta de dados é um diferencial em comparação com os outros sites de analise dos Royalties. Alguns exemplos: OmeuMunincipio ( apenas dados do Siconf), InfoRoyalties da CandidoMendes (apenas as transferencia da ANP). A nossa coleta permite a analise completa dos dados referentes ao Petroleo, incluindo as transferencias pelos Estados, as Relações Onerosas e ainda permite a eliminação dos royalties de Minerio e Hídrico.
(3) A coleta de dados permite a conferencias dos dados informados sobre os Royalties transferidos e recebidos, comparando os dados informados pela União, pelo Estado, pelo ANP e pelo Municipio(Sinconf)."""),



                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
                                            'margin': '5px'
                                        }
                                    ),
                
                 
                ],
            className = "row container-display",
            style={'flex-wrap': 'wrap', 'align-items': 'stretch', 'margin':'0px -4px'}
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
                                    value = 'NUPEC',
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS]+[{'label':'NUPEC', 'value':'NUPEC'},{'label':'NORTE', 'value':'NORTE'},{'label':'CENTRO', 'value':'CENTRO'}],
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
                                            'width': '100%',
                                            'margin': '5px'
                                        }
                                    ),

                                                    html.Div([  ## grafico 2
                 
                           
                                    dcc.Graph(className = "graph", id = 'my-graph-ods-2', figure = graf_ods_2(NUPEC)),

  
                                            html.P("xxxx"),
                                            html.P("Fonte: xxx")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
                                            'margin': '5px'
                                        }
                                    ),
                
                 
                ],
            className = "row container-display",
            style={'flex-wrap': 'wrap', 'align-items': 'stretch', 'margin':'0px -4px'}
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
                                    value = 'NUPEC',
                                    options=[{'label':name, 'value':name} for name in MUNICIPIOS]+[{'label':'NUPEC', 'value':'NUPEC'},{'label':'NORTE', 'value':'NORTE'},{'label':'CENTRO', 'value':'CENTRO'}],
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
                                            html.P("Gasto com saúde proporcional à população do município."), 
                                             html.P("Fonte: SICONFI, Ministério da Saúde (https://covid.saude.gov.br/) e IBGE")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
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
                                            html.P("Comparativo de gasto de Saúde com óbitos e casos de COVID 19. Maiores gastos representaram melhor qualidade dos serviços de saúde nos municípios?"),
                                            html.P("Fonte: SICONFI, Ministério da Saúde (https://covid.saude.gov.br/) e IBGE")
                                        ],
                                        className = "pretty_container", style = {
                                            'width': '100%',
                                            'margin': '5px'
                                        }
                                    ),
                ],
            className = "row container-display",
            style={'flex-wrap': 'wrap', 'align-items': 'stretch', 'margin':'0px -4px'}
        ),
      
])

])

outros_links = html.Div([html.Div(outroslinks(html,app))], style={'padding': '20px','background-color':'#fff','border':'1px solid lightgrey'})

# index layout
app.layout = base
app.validation_layout = html.Div([base,pagina_inicial,dados_socioeconomicos,financeiro,royalties,ods,saude,outros_links])

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


@app.callback(Output('my-graph-soc','figure'),[Input('filtro-local','value'),Input('filtro-funcao-soc','value')])
def update_graph_soc(local,funcao):
    return graf_soc(local,funcao)

@app.callback(Output('my-graph-fin-1','figure'),[Input('filtro-local-fin','value'),Input('filtro-funcao-fin','value')])
def update_graph_fin_1(local,funcao):
    return graf_fin_1(local,funcao)

@app.callback(Output('my-graph-fin-2','figure'),[Input('filtro-local-fin','value'),Input('filtro-funcao1-fin','value'),Input('filtro-funcao2-fin','value')])
def update_graph_fin_2(local,funcao1,funcao2):
    return graf_fin_2(local,funcao1,funcao2)

@app.callback(Output('my-graph-fin-3','figure'),[Input('filtro-local-fin','value'),Input('filtro-funcao1B-fin','value'),Input('filtro-funcao2B-fin','value')])
def update_graph_fin_3(local,funcao1,funcao2):
    return graf_fin_3(local,funcao1,funcao2)

@app.callback(Output('my-graph-roy-1','figure'),[Input('filtro-local-roy','value')])
def update_graph_roy_1(local):
    return graf_roy_1(local)

@app.callback(Output('my-graph-roy-2','figure'),[Input('filtro-local-roy','value')])
def update_graph_roy_2(local):
    return graf_roy_2(local)

@app.callback(Output('my-graph-roy-3','figure'),[Input('filtro-local-roy','value'),Input('filtro-detalhe-roy','value')])
def update_graph_roy_3(local,detalhe):
    return graf_roy_3(local,detalhe)


@app.callback([Output('my-graph-ods-1','figure'),Output('my-graph-ods-2','figure')],[Input('filtro-local-ods','value')])
def update_graph_ods_1(local):
    return graf_ods_1(local),graf_ods_2(local)

@app.callback(Output('my-graph-saude-1','figure'),[Input('filtro-local-saude','value'),Input('filtro-funcao-saude','value')])
def update_graph_saude_1(local,funcao):
    return graf_saude_1(local)

@app.callback(Output('my-graph-saude-2','figure'),[Input('filtro-local-saude','value'),Input('filtro-funcao-saude','value')])
def update_graph_saude_2(local,funcao):
    return  graf_saude_2(local,funcao) 
