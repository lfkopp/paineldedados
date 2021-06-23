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
# Create MUNICIPIOS
MUNICIPIOS = []
NUM_MUN = len(RJ_MUN_GEOJSON["features"])
for i in range(NUM_MUN):
    MUNICIPIOS.append(RJ_MUN_GEOJSON["features"][i]["properties"]["name"])

NUPEC = ['Areal','Armação dos Búzios','Miguel Pereira','Paraíba do Sul','Paty dos Alferes','Quissamã','Rio das Flores','Sapucaia','Saquarema','Três Rios','Vassouras']

financeiros = ["Despesas Exceto Intraorçamentárias","01 - Legislativa","04 - Administração","06 - Segurança Pública","08 - Assistência Social","09 - Previdência Social",
				"10 - Saúde","12 - Educação","15 - Urbanismo","17 - Saneamento","20 - Agricultura","23 - Comércio e Serviços","26 - Transporte","28 - Encargos Especiais","Outros"]


# Filter definitions

# Graphs

#@cache.memoize(timeout=timeout)  # in seconds
def graf1(local=""):
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
def graf2(local=""):
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
	fig =  px.scatter(df, x=funcao1, y=funcao2, color="municipio", hover_data=['municipio','ano'], title="Graf. 2 - Correlação entre dois tipos de Despesas")
	return fig  

def graf_roy_1(local):
	df = ROYALTIES
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.line(df, x='ano', y='Royalties', color="municipio", hover_data=['municipio','ano'], title="Graf. 1 - Evolução Anual de Royalties")
	return fig  

def graf_roy_2(local):
	df = ROYALTIES
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.line(df, x='ano', y='royalties per capita', color="municipio", hover_data=['municipio','ano'], title="Graf. 2 - Evolução Anual de Royalties per capita")
	return fig  