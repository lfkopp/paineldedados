from app.config import cache, timeout
import pandas as pd
import numpy as np
from datetime import datetime as dt
from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.express as px
import plotly.io as pio
import json
import pathlib
from unicodedata import normalize
 
def remover_acentos(txt):
	return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()


PATH = pathlib.Path(__file__).parent

px.set_mapbox_access_token("pk.eyJ1Ijoicm1jbnJpYmVpcm8iLCJhIjoiY2s4MHh5b3ZiMGtsbTNkcGFuazR1dWc4diJ9._aDTNPlmw3Nt6QSMm3YgmQ")

with open(PATH.joinpath('data/geojs-33-mun.json'),encoding='utf-8') as geojson:
    RJ_MUN_GEOJSON = json.load(geojson)

FINBRA_ = PATH.joinpath("data/finbra_desp.csv")
FINBRA = pd.read_csv(FINBRA_, sep=";",index_col=False)

ROYALTIES_ = PATH.joinpath("data/royalties.csv")
ROYALTIES = pd.read_csv(ROYALTIES_, sep=";",index_col=False)

POP_ = PATH.joinpath("data/populacao.csv")
POP = pd.read_csv(POP_, sep=";",index_col=False)

SAUDE_ = PATH.joinpath("data/saude.csv")
SAUDE = pd.read_csv(SAUDE_)

OUTROS_ = PATH.joinpath("data/outroslinks.xlsx")
OUTROS = pd.read_excel(OUTROS_)

# Create MUNICIPIOS
MUNICIPIOS = []
NUM_MUN = len(RJ_MUN_GEOJSON["features"])
for i in range(NUM_MUN):
    MUNICIPIOS.append(RJ_MUN_GEOJSON["features"][i]["properties"]["name"])

NUPEC = ['Areal','Armação dos Búzios','Miguel Pereira','Paraíba do Sul','Paty dos Alferes','Quissamã','Rio das Flores','Sapucaia','Saquarema','Três Rios','Vassouras']

financeiros = ["Despesas Exceto Intraorçamentárias","01 - Legislativa","04 - Administração","06 - Segurança Pública","08 - Assistência Social","09 - Previdência Social",
				"10 - Saúde","12 - Educação","15 - Urbanismo","17 - Saneamento","20 - Agricultura","23 - Comércio e Serviços","26 - Transporte","28 - Encargos Especiais","Outros"]

saudes = ['casos','obitos','casopor100k','obitopor100k','pop','saude','letalidade','saudepop']
# Filter definitions

# Graphs

#@cache.memoize(timeout=timeout)  # in seconds
def graf1(local=NUPEC):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	dados_file = PATH.joinpath("data/IDHM.csv")
	df = pd.read_csv(dados_file, sep=";",index_col=False)
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['nome'].isin(local)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations="nome",
							featureidkey = 'properties.name',
							color="IDHM",
							hover_name="nome",
							color_continuous_scale="YlGn",
							#range_color=(.450, .800),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							animation_frame='ano',
							labels={'IDHM':'IDH Municipal'}
                          	)
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'Graf. 1 - índice de Desenvolvimento Humano Municipal do RJ',
							'x':0.5,
							'yanchor': 'top'},
							paper_bgcolor='#f5f5f5',
							margin={'t':50,'b':40,'l':20,'r':20},
							legend_orientation="h")
	fig.layout['sliders'][0]['active'] = len(fig.layout['sliders'][0]['steps'])-1
	return fig
 
#@cache.memoize(timeout=timeout)  # in seconds
def graf2(local=NUPEC):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	dados_file = PATH.joinpath("data/gini.csv")
	df = pd.read_csv(dados_file, sep=";",dtype={"id": str},index_col=False)
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['nome'].isin(local)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations="nome",
							featureidkey = 'properties.name',
							color="gini",
							hover_name="nome",
							color_continuous_scale="YlGn_r",
							#range_color=(0.4, 0.65),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							animation_frame='ano',
							labels={'gini':'GINI'}
							)
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'Graf. 2 - índice de Gini dos Municípios do RJ',
							'x':0.5,
							'yanchor': 'top'},
							paper_bgcolor='#f5f5f5',
							margin={'t':50,'b':40,'l':20,'r':20},
							legend_orientation="h")
	fig.layout['sliders'][0]['active'] = len(fig.layout['sliders'][0]['steps'])-1
	return fig

#@cache.memoize(timeout=timeout) 
def graf3(local=NUPEC):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	df = POP 
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations="municipio",
							featureidkey = "properties.name",
							color="populacao",
							hover_name="municipio",
							color_continuous_scale="YlGn",
							#range_color=(0.4, 0.65),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							animation_frame='ano',
							labels={'populacao':'populacao'},
							)
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'Graf. 3 - População dos Municípios do RJ',
							'x':0.75,
							'yanchor': 'top'},
							paper_bgcolor='#f5f5f5',
							margin={'t':50,'b':40,'l':20,'r':20},
							legend_orientation="h")

	fig.layout['sliders'][0]['active'] = len(fig.layout['sliders'][0]['steps'])-1
	return fig

#@cache.memoize(timeout=timeout) 
def graf4(local=NUPEC):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	df = POP
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.scatter(df, x='ano', y='populacao', color="municipio", trendline="ols", hover_data=['municipio','ano'], title="Graf. 4 - ano pop")
	fig.update_layout(paper_bgcolor='#f5f5f5')
	return fig  


#@cache.memoize(timeout=timeout)  # in seconds
def graf_fin_1(local="",funcao="Despesas Exceto Intraorçamentárias"):
	df = FINBRA
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x) for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig =  px.line(df, x="ano", y=funcao, color='municipio', title="Graf. 1 - Evolução Anual de Despesas")
	return fig
 

def graf_fin_2(local="",funcao1="10 - Saúde", funcao2="12 - Educação"):
	df = FINBRA
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x) for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig =  px.scatter(df, x=funcao1, y=funcao2, color="municipio", trendline="ols", hover_data=['municipio','ano'], title="Graf. 2 - Correlação entre dois tipos de Despesas")
	return fig  

def graf_roy_1(local):
	df = ROYALTIES 
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.line(df, x='ano', y='Royalties', color="municipio", hover_data=['municipio','ano'], title="Graf. 1 - Evolução Anual de Royalties")
	fig.update_layout(xaxis = dict(tickmode = 'linear',dtick = 1))
	return fig  

def graf_roy_2(local):
	df = ROYALTIES
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.line(df, x='ano', y='royalties per capita',  color="municipio", hover_data=['municipio','ano'], title="Graf. 2 - Evolução Anual de Royalties per capita")
	fig.update_layout(xaxis = dict(tickmode = 'linear',dtick = 1))
	return fig  

def graf_ods_1(local):
	df = ROYALTIES
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.density_heatmap(df, x='ano', z='royalties per capita',  y="municipio", hover_data=['municipio','ano'], title="Graf. 1 - Metas ODS")
	fig.update_layout(xaxis = dict(tickmode = 'linear',dtick = 1))
	return fig  

def graf_ods_2(local):
	df = ROYALTIES
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.density_heatmap(df, x='ano', z='royalties per capita',  y="municipio", hover_data=['municipio','ano'], title="Graf. 1 - Metas ODS")
	fig.update_layout(xaxis = dict(tickmode = 'linear',dtick = 1))
	return fig  

def graf_saude_1(local):
	df = SAUDE
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x).upper() for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig = px.scatter(df, x='pop', y='saude', color='municipio', hover_data=['municipio','ano'], title="Graf. 1 -  Gasto de saúde per capita x População em 2019")
	return fig

def graf_saude_2(local, funcao='obitopor100k'):
	df = SAUDE
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x).upper() for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig = px.scatter(df, x='saudepop', y=funcao, color='municipio',  hover_data=['municipio','ano'], title="Graf. 2 - Indicador selecionado x Gasto de saúde per capita")
	return fig


def outroslinks(html,app):
	result = [] 
	result.append(html.Hr())

	for line in OUTROS.iterrows():
		print()
		result.append(    
			html.Div([   ## primeiro frame
        
       		html.Div([html.P(html.Img(src=app.get_asset_url("outroslinks/"+i), width=300)) for i in line[1]['imagens'].split(',') ]),

        	html.Div([html.H4(html.A([line[1]['local']], target='_blank', href=line[1]['link'], style={"color": "red", "text-decoration": "none"})),
					html.Div( [html.P(x) for x in line[1]['descricao'].split('\n')] )
						],

            style = {
                'margin-bottom': '10px',
                'margin-left': '40px',
                'margin-right': '4px'
            }
					
					),

			
        
        ],
        className = "row container-display",
            style = {
                'margin-bottom': '10px',
                'margin-left': '4px',
                'margin-right': '-4px'
            }))
		result.append(html.Hr())
	return result
 
