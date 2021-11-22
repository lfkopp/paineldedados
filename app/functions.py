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

#px.set_mapbox_access_token("pk.eyJ1Ijoicm1jbnJpYmVpcm8iLCJhIjoiY2s4MHh5b3ZiMGtsbTNkcGFuazR1dWc4diJ9._aDTNPlmw3Nt6QSMm3YgmQ")
px.set_mapbox_access_token("pk.eyJ1IjoibGZrb3BwMTIzIiwiYSI6ImNrcnZobG01bTA2cWgybm8zcjhsbGNoMWEifQ.i3x7c9tzoJnNdpSFzMTUXA.MDfulIl0SWa2laZ1IrRs8w")
with open(PATH.joinpath('data/geojs-33-mun.json'),encoding='utf-8') as geojson:
    RJ_MUN_GEOJSON = json.load(geojson)

FINBRA_ = PATH.joinpath("data/finbra_desp.csv")
FINBRA = pd.read_csv(FINBRA_, sep=";",index_col=False)

ROYALTIES_ = PATH.joinpath("data/royalties.csv")
ROYALTIES = pd.read_csv(ROYALTIES_, sep=";",index_col=False)

ROYALTIESDET_ = PATH.joinpath("data/royalties_detalhe.csv")
ROYALTIESDET = pd.read_csv(ROYALTIESDET_, sep=";",index_col=False)

POP_ = PATH.joinpath("data/populacao.csv")
POP = pd.read_csv(POP_, sep=";",index_col=False)

SAUDE_ = PATH.joinpath("data/saude.csv")
SAUDE = pd.read_csv(SAUDE_)

AREA_ = PATH.joinpath("data/area.csv")
AREA = pd.read_csv(AREA_, sep=';',decimal=',', index_col=False, nrows=92)
AREA = POP.merge(AREA, on='municipio')
AREA['densidade'] = AREA['populacao'] / AREA['area']

IDEB_ = PATH.joinpath("data/ideb.xlsx")
IDEB = pd.read_excel(IDEB_)
IDEB = IDEB[IDEB['serie'] == '5 ano']
IDEB['municipio'] = IDEB['municipio'].apply(remover_acentos)

IDHM_  = PATH.joinpath("data/IDHM.csv")
IDHM = pd.read_csv(IDHM_, sep=";",index_col=False)

GINI_ = PATH.joinpath("data/gini.csv")
GINI = pd.read_csv(GINI_, sep=";",dtype={"id": str},index_col=False)

EFICIENCIA_ = PATH.joinpath("data/despesas_do_resumo.xlsx")
EFICIENCIA = pd.read_excel(EFICIENCIA_)
for x in ["Despesas Correntes","Despesas de Capital","Investimentos","Pessoal"]:
	EFICIENCIA['% '+x] = EFICIENCIA[x]/EFICIENCIA['total']
ROYALTIES_TEMP = ROYALTIES.copy()
ROYALTIES_TEMP['municipio'] = ROYALTIES_TEMP['municipio'].apply(remover_acentos)
EFICIENCIA = pd.merge(EFICIENCIA, ROYALTIES_TEMP, how='left', on=['municipio','ano'])
EFICIENCIA.fillna(0, inplace=True)
EFICIENCIA

OUTROS_ = PATH.joinpath("data/outroslinks.xlsx")
OUTROS = pd.read_excel(OUTROS_)


# Create MUNICIPIOS
MUNICIPIOS = []
NUM_MUN = len(RJ_MUN_GEOJSON["features"])
for i in range(NUM_MUN):
    MUNICIPIOS.append(RJ_MUN_GEOJSON["features"][i]["properties"]["name"])

NUPEC = ['Areal','Armação dos Búzios','Casimiro de Abreu','Comendador Levy Gasparian','Iguaba Grande','Miguel Pereira','Paraíba do Sul','Quissamã','Rio Claro','Rio das Flores','São Pedro da Aldeia', 'Sapucaia','Saquarema','Três Rios']

	
# 'Vassouras','Paty dos Alferes',

financeiros = ["Despesas Exceto Intraorçamentárias","01 - Legislativa","04 - Administração","06 - Segurança Pública","08 - Assistência Social","09 - Previdência Social",
				"10 - Saúde","12 - Educação","15 - Urbanismo","17 - Saneamento","20 - Agricultura","23 - Comércio e Serviços","26 - Transporte","28 - Encargos Especiais","Outros"]

eficiencias = [ "total","Despesas Correntes","Despesas de Capital","Investimentos","Pessoal","% Despesas Correntes","% Despesas de Capital","% Investimentos","% Pessoal","Royalties", "pop", "royalties per capita"]

saudes = ['casos','obitos','casopor100k','obitopor100k','pop','saude','letalidade','saudepop']

detalhes_roy = ['Royalties Estado','Cessão Onerosa - PBAM','Royalties - ANP','Royalties - CFH','Royalties - CFM','Royalties - FEP','Royalties - PEA','Total Geral']

opt_soc = {	'IDHM':{ 		'label':'IDH Municipal', 				'hover':'nome', 'name':'IDHM',		'col':'IDHM', 'filename':IDHM, 'desc':'oi tudo bem', 	'fonte':'http://www.atlasbrasil.org.br/'},
			'GINI':{ 		'label':'Índice Gini', 					'hover':'nome',      'name':'GINI', 		'col':'gini', 'filename':GINI, 'desc':'oi tudo bem2', 	'fonte':'IBGE'},
			'DENSIDADE':{ 	'label':'Densidade Populacional', 		'hover':'municipio', 'name':'DENSIDADE', 'col':'densidade', 'filename':AREA, 'desc':'oi tudo bem2', 	'fonte':'IBGE'},
			'POPULACAO':{	'label':'População', 					'hover':'municipio', 'name':'POPULACAO',	'col':'populacao', 'filename':POP, 'desc':'oi tudo bem2', 	'fonte':'IBGE'},
			'ROYALTIES':{	'label':'Royalties', 					'hover':'municipio', 'name':'ROYALTIES',	'col':'Royalties', 'filename':ROYALTIES, 'desc':'oi tudo bem2', 	'fonte':'ANP, SICONFI'},
			'IDEB':{ 		'label':'Nota IDEB para quinto ano', 	'hover':'mun', 'name':'IDEB', 		'col':'nota', 'filename':IDEB, 'desc':'oi tudo bem2', 	'fonte':'http://ideb.inep.gov.br/'},
			'IDEB_100':{ 	'label':'Nota IDEB para quinto ano pardronizada', 	'hover':'mun', 'name':'IDEB_100', 		'col':'nota_100', 'filename':IDEB, 'desc':'oi tudo bem2', 	'fonte':'http://ideb.inep.gov.br/'}}

# Filter definitions

# Graphs
#@cache.memoize(timeout=timeout)  # in seconds
def graf_soc(local=NUPEC, funcao='GINI'):
	if 'NUPEC' in local:
		local = [remover_acentos(x).upper() for x in list(set(list(NUPEC) + list(local)))]
	df = opt_soc[funcao]['filename']
	mmin,mmax = min(df[opt_soc[funcao]['col']]),max(df[opt_soc[funcao]['col']])
	df['MUN'] =df[opt_soc[funcao]['hover']].apply(lambda x: remover_acentos(x).upper())
	if (type(local) == list) and (len(local)>0):
		local = [remover_acentos(x).upper() for x in local]
		df = df.loc[df['MUN'].isin(local)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations=opt_soc[funcao]['hover'],
							featureidkey = 'properties.name',
							color=opt_soc[funcao]['col'],
							hover_name=opt_soc[funcao]['hover'],
							color_continuous_scale="YlGn",
							range_color=(mmin, mmax),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							animation_frame='ano',
							labels={opt_soc[funcao]['col']:opt_soc[funcao]['label']}
                          	)
	texto = f"""<b>{opt_soc[funcao]['label']}</b><br>fonte: {opt_soc[funcao]['fonte']}<br>"""
	fig.update_geos(fitbounds="locations",visible=False).update_layout(
		title={'text':texto,
							'x':0.5,
							'yanchor': 'top'},
							paper_bgcolor='#f5f5f5',
							margin={'t':60,'b':40,'l':20,'r':20},
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
	fig =  px.scatter(df, x=funcao1, y=funcao2, color="municipio", trendline="ols", hover_data=['municipio','ano'], title="Graf. 2 - Correlação entre dois tipos de Despesas por função")
	return fig  


def graf_fin_3(local="",funcao1="total", funcao2="Despesas Correntes"):
	df = EFICIENCIA
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x) for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig =  px.scatter(df, x=funcao1, y=funcao2, color="municipio", trendline="ols", hover_data=['municipio','ano'], title="Graf. 3 - Correlação entre dois tipos de Despesas")
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

def graf_roy_3(local,detalhe="Total Geral"):
	df = ROYALTIESDET
	local = [remover_acentos(x).upper() for x in local]
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig =  px.line(df, x='ano', y=detalhe,  color="municipio", hover_data=['municipio','ano'], title="Graf. 3 - Evolução Anual de Royalties por tipo")
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
	for line in OUTROS.iterrows():
		result.append(    
			html.Div([ 
            	html.Div([html.P(html.Img(src=app.get_asset_url("outroslinks/"+i), width=300)) for i in line[1]['imagens'].split(',') ]),
	        	html.Div([html.H4(html.A([line[1]['local']], target='_blank', href=line[1]['link'], style={"color": "red", "text-decoration": "none"})),
				html.Div([html.P(x) for x in line[1]['descricao'].split('\n')])],style = {'margin-bottom': '10px','margin-left': '40px','margin-right': '4px'}),],className = "row container-display",style = {'margin-bottom': '10px','margin-left': '4px','margin-right': '-4px'}))
		result.append(html.Hr())
	return result
 
def fotos_prof(app,html):
	result = []
	profs = ['Ariane Figueira', 'Eduardo Raupp', 'Olavo Diogo', 'Marie Anne Macadar']
	for p in profs:
		p2 = p.replace(' ','_')
		result.append(html.Div([
                    html.Img(src = app.get_asset_url('pessoas/'+p2+'.jpg'),id = p2+"-image",title = p, className = "fotinha"),
                    html.P([p])],style = {'margin':'6px'}))
	return result

def fotos_assist(app,html):
	result = []
	profs = ['Luis Filipe Kopp', 'Helena Dias', 'Vanessa', 'Matheus Paiva']
	for p in profs:
		p2 = p.replace(' ','_')
		result.append(html.Div([
                    html.Img(src = app.get_asset_url('no-user.png'),id = p2+"-image",title = p, className = "fotinha"),
                    html.P([p])],style = {'margin':'6px'}))
	return result