#%%
import pandas as pd
import pathlib
from unicodedata import normalize
PATH = pathlib.Path(__file__).parent
# %%
FINBRA_ = PATH.joinpath("data/finbra_desp.csv")
FINBRA = pd.read_csv(FINBRA_, sep=";",index_col=False)

ROYALTIES_ = PATH.joinpath("data/royalties.csv")
ROYALTIES = pd.read_csv(ROYALTIES_, sep=";",index_col=False)
# %%
FINBRA
# %%
ROYALTIES
# %%
def remover_acentos(txt):
	return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

ROYALTIES['municipio'] = ROYALTIES['municipio'].apply(remover_acentos)
# %%
df  = pd.merge(FINBRA,ROYALTIES, on=['municipio','ano'])
# %%
df = df[['municipio','ano','Despesas Exceto Intraorçamentárias','Royalties','10 - Saúde','12 - Educação']]
# %%
import matplotlib.pyplot as plt
# %%
plt.scatter(df['Royalties'],df['10 - Saúde'])
# %%
plt.scatter(df['Royalties'],df['12 - Educação'])

# %%
df.to_excel('finbra_roy2.xlsx')
# %%
opt_soc = {	'IDHM':{'funcao':'f', 'name':'IDHM', 'desc':'oi tudo bem', 'fonte':'esa é uma fonte'},
			'IDHM2':{'funcao':'f', 'name':'IDHM2', 'desc':'oi tudo bem2', 'fonte':'esa é uma fonte2'}}
# %%
[x for x in opt_soc.keys()]
# %%
import pandas as pd
import pathlib
from unicodedata import normalize
PATH = pathlib.Path(__file__).parent

def remover_acentos(txt):
	return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()


# %%
ROYALTIES_ = PATH.joinpath("data/royalties.csv")
ROYALTIES = pd.read_csv(ROYALTIES_, sep=";",index_col=False)


EFICIENCIA_ = PATH.joinpath("data/despesas_do_resumo.xlsx")
EFICIENCIA = pd.read_excel(EFICIENCIA_)
for x in ["Despesas Correntes","Despesas de Capital","Investimentos","Pessoal"]:
	EFICIENCIA['% '+x] = EFICIENCIA[x]/EFICIENCIA['total']
ROYALTIES_TEMP = ROYALTIES
ROYALTIES_TEMP['municipio'] = ROYALTIES_TEMP['municipio'].apply(remover_acentos)
EFICIENCIA = pd.merge(EFICIENCIA, ROYALTIES_TEMP, how='left', on=['municipio','ano'])
EFICIENCIA.fillna(0, inplace=True)
EFICIENCIA
# %%
def graf2(local=NUPEC):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	df = GINI
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
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'<b>Gráfico: '+opt_soc['GINI']['label']+'</b><br>fonte: '+opt_soc['GINI']['fonte'],
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
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'<b>Gráfico: '+opt_soc['POPULACAO']['label']+'</b><br>fonte: '+opt_soc['POPULACAO']['fonte'],
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
	df = AREA 
	if (type(local) == list) and (len(local)>0):
		df = df.loc[df['municipio'].isin(local)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations="municipio",
							featureidkey = "properties.name",
							color="densidade",
							hover_name="municipio",
							color_continuous_scale="YlGn",
							animation_frame='ano',
							#range_color=(0.4, 0.65),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							labels={'densidade':'densidade'},
							)
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'<b>Gráfico: '+opt_soc['DENSIDADE']['label']+'</b><br>fonte: '+opt_soc['DENSIDADE']['fonte'],
							'x':0.75,
							'yanchor': 'top'},  
							paper_bgcolor='#f5f5f5',
							margin={'t':50,'b':40,'l':20,'r':20},
							legend_orientation="h")
	return fig


#@cache.memoize(timeout=timeout) 
def graf5(local=NUPEC,serie='5 ano'):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	df = IDEB
	df['municipio'] = df['municipio'].apply(remover_acentos)
	df = df[df['serie'] == serie]
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x) for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations="mun",
							featureidkey = "properties.name",
							color="nota",
							hover_name="municipio",
							color_continuous_scale="YlGn",
							animation_frame='ano',
							range_color=(2, 7),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							labels={'nota':'nota'},
							)
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'<b>Gráfico: '+opt_soc['IDEB']['label']+'</b><br>fonte: '+opt_soc['IDEB']['fonte'],
							'x':0.75,
							'yanchor': 'top'},  
							paper_bgcolor='#f5f5f5',
							margin={'t':50,'b':40,'l':20,'r':20},
							legend_orientation="h")
	return fig

#@cache.memoize(timeout=timeout) 
def graf6(local=NUPEC):
	if 'NUPEC' in local:
		local = list(set(list(NUPEC) + list(local)))
	df = ROYALTIES
	df['municipio'] = df['municipio'].apply(remover_acentos)
	if (type(local) == list) and (len(local)>0):
		local2 = [remover_acentos(x).upper() for x in local]
		df = df.loc[df['municipio'].isin(local2)]
	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations="municipio",
							featureidkey = "properties.nome",
							color="Royalties",
							hover_name="municipio",
							color_continuous_scale="YlGn",
							animation_frame='ano',
							#range_color=(2, 7),
							mapbox_style="carto-positron",
							zoom=6, center=dict(lat=-22.158536, lon=-42.684229),
							opacity=0.5,
							labels={'Royalties':'Royalties'},
							)
	fig.update_geos(fitbounds="locations",visible=False).update_layout(title={'text':'<b>Gráfico: '+opt_soc['ROYALTIES']['label']+'</b><br>fonte: '+opt_soc['ROYALTIES']['fonte'],
							'x':0.75,
							'yanchor': 'top'},  
							paper_bgcolor='#f5f5f5',
							margin={'t':50,'b':40,'l':20,'r':20},
							legend_orientation="h")
	return fig

def graf_soc(local=NUPEC,funcao='IDHM'):
	if funcao == 'IDHM':
		return graf1(local)
	elif funcao == 'GINI':
		return graf2(local)
	elif funcao == 'POPULACAO':
		return graf3(local)
	elif funcao == 'DENSIDADE':
		return graf4(local)
	elif funcao == 'IDEB':
		return graf5(local)
	elif funcao == 'ROYALTIES':
		return graf6(local)
	else:	
		return "por favor, selecione um indicador"