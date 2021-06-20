# Imports
from app.config import cache, timeout
import math
import pandas as pd
import numpy as np
from datetime import datetime as dt
from os.path import getmtime
from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.express as px
import plotly.io as pio
import json
import unidecode
import pathlib
from scipy.ndimage import gaussian_filter
import scipy.special as sp
from scipy import stats as sps
from scipy.interpolate import interp1d
from scipy.integrate import odeint
from sklearn.linear_model import LinearRegression

# Set path
PATH = pathlib.Path(__file__).parent

# APIs
px.set_mapbox_access_token("pk.eyJ1Ijoicm1jbnJpYmVpcm8iLCJhIjoiY2s4MHh5b3ZiMGtsbTNkcGFuazR1dWc4diJ9._aDTNPlmw3Nt6QSMm3YgmQ")

# Data
with open(PATH.joinpath('data/municipios_rj.min.json'),encoding='utf-8') as geojson:
    RJ_MUN_GEOJSON = json.load(geojson)

dados_file = PATH.joinpath("data/dados_covid.csv")
SE_file = PATH.joinpath("data/SE.csv")
dados_covid = pd.read_csv(dados_file, sep=";")

dados_covid['dataNotificacao'] = pd.to_datetime(dados_covid['dataNotificacao'], utc=False,dayfirst=True).dt.date
dados_covid['dataInicioSintomas'] = pd.to_datetime(dados_covid['dataInicioSintomas'], utc=False,dayfirst=True).dt.date

latest_date = dt.fromtimestamp(getmtime(dados_file)).strftime('%d/%m/%Y')
most_recent = dt.strptime(str(max(list(dados_covid['dataNotificacao'].unique()))), '%Y-%m-%d').strftime('%d/%m/%Y')

# Create MUNICIPIOS
MUNICIPIOS = []
NUM_MUN = len(RJ_MUN_GEOJSON["features"])
for i in range(NUM_MUN):
    MUNICIPIOS.append(RJ_MUN_GEOJSON["features"][i]["properties"]["name"])

MUN_DICT_G2D = {}
MUN_DICT_D2G = {}
for cidade in MUNICIPIOS:
	MUN_DICT_G2D[str(cidade)] = str((unidecode.unidecode(cidade)).upper())
	MUN_DICT_D2G[str((unidecode.unidecode(cidade)).upper())] = str(cidade)

# Filter definitions
@cache.memoize(timeout=timeout)  # in seconds
def filtra_info(df,sex,age,local,classificacao,data1,data2,uf):
	# df = df.loc[(pd.to_datetime(df.data) >= pd.to_datetime(data1)) & (pd.to_datetime(df.data) <= pd.to_datetime(data2))]
	age.sort()
	if len(uf) != 0:
		df = df.loc[df['estado'].isin(uf)]
		if len(local) != 0:
			df = df.loc[df['municipio'].isin(local)]
	if len(age) != 5:
		if len(age) != 0:
			df = df.loc[df.idade >= int(age[0][0:2])]
			if int(age[-1][-2:]) != 60:
				df = df.loc[df.idade <= int(age[-1][-2:])]
	if sex == ['F']:
		df = df.loc[df['sexo'] == 'F']
	if sex == ['M']:
		df = df.loc[df['sexo'] == 'M']
	return df

def filtra_graph(df,sex,age,local,classificacao,data1,data2,uf):
	if len(classificacao) !=0 :
		df = df.loc[df['classificacaoFinal'].isin(classificacao)]
	# df = df.loc[(pd.to_datetime(df.data) >= pd.to_datetime(data1)) & (pd.to_datetime(df.data) <= pd.to_datetime(data2))]
	age.sort()
	if len(uf) != 0:
		df = df.loc[df['estado'].isin(uf)]
		if len(local) != 0:
			df = df.loc[df['municipio'].isin(local)]
	if len(age) != 0:
		df = df.loc[df.idade >= int(age[0][0:2])]
		if int(age[-1][-2:]) != 60:
			df = df.loc[df.idade <= int(age[-1][-2:])]
	if sex == ['F']:
		df = df.loc[df['sexo'] == 'F']
	if sex == ['M']:
		df = df.loc[df['sexo'] == 'M']
	return df

def filtra_scatter(df,idade,sexo,uf,mun):
    if len(uf) != 0:
        df = df.loc[df['estado'].isin(uf)]
        if len(mun) != 0:
            df = df.loc[df['municipio'].isin(mun)]
    if len(idade) != 0:
        df = df.loc[df.idade >= int(idade[0][0:2])]
    if sexo == ['F']:
        df = df.loc[df['sexo'] == 'F']
    if sexo == ['M']:
        df = df.loc[df['sexo'] == 'M']
    return df

# R0
SEs = pd.read_csv(SE_file, sep=",")

SEs['Inicio_SE'] = pd.to_datetime(SEs['Inicio_SE'], format="%Y-%m-%d")
SEs['Fim_SE'] = pd.to_datetime(SEs['Fim_SE'], format="%Y-%m-%d")

dataStatus = dados_covid[['dataNotificacao','classificacaoFinal']]

dataStatus_ = dataStatus.dropna(axis=0)
dataStatus_["value"]=1
dataStatus_['dataNotificacao']=pd.to_datetime(dataStatus_['dataNotificacao'])
dataStatus_=dataStatus_.loc[dataStatus_['classificacaoFinal']=="CONFIRMADO",:]

situacao = dataStatus_.pivot_table(index='dataNotificacao', columns='classificacaoFinal', values="value", aggfunc='sum').resample('d').sum()

situacao["CONFIRMADO_ACUM"] = situacao["CONFIRMADO"].cumsum()

@cache.memoize(timeout=timeout)  # in seconds
def LAST_SE(SEs, situacao):
    
    last_se = 0
    
    for SEpid in SEs["SE"].values:
        
        Inicio = pd.to_datetime(SEs.loc[SEs["SE"]==SEpid].Inicio_SE)
        Inicio = Inicio.dt.strftime("%Y-%m-%d").values[0]

        Fim = pd.to_datetime(SEs.loc[SEs["SE"]==SEpid].Fim_SE)
        Fim = Fim.dt.strftime("%Y-%m-%d").values[0]
        
        if (str(situacao.index[-1])[:10] in pd.date_range(start=Inicio, end=Fim)):
            last_se = SEpid - 1
        
    return last_se

@cache.memoize(timeout=timeout)  # in seconds
def LISTA_CONF_SE(SEs, last_se, situacao):
    lista_acum = []


    for i in range(SEs["SE"][0], last_se + 1, 1):

        Inicio = SEs.loc[SEs["SE"]==i].Inicio_SE
        Inicio = Inicio.dt.strftime("%Y-%m-%d").values[0]

        Fim = SEs.loc[SEs["SE"]==i].Fim_SE
        Fim = Fim.dt.strftime("%Y-%m-%d").values[0]

        acum = situacao.loc[Inicio:Fim,"CONFIRMADO"].cumsum()
        lista_acum.append(acum[-1])

    return lista_acum

@cache.memoize(timeout=timeout)  # in seconds
def calcula_r(g):
    
    R_T_MAX = 12
    r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)
    
    h = gaussian_filter(g, 4)
    #h = g
    #print(h)

    lam = h[:-1] * np.exp(1/5.2 * (r_t_range[:, None] - 1))
    likelihood_r_t = sps.poisson.pmf(h[1:], lam)
    likelihood_r_t /= np.sum(likelihood_r_t, axis=0)

#    ax = pd.DataFrame(
#        data = likelihood_r_t,
#        index = r_t_range
#    ).plot(
#        title='Likelihood de $R_t$ dado $k$',
#        xlim=(0,10),
#        figsize=(12,2.5)
#    )
#    ax.legend(labels=h[1:], title='Novos casos por semanas')
#    ax.set_xlabel('$R_t$');

    teste = pd.DataFrame(
        data = likelihood_r_t,
        index = r_t_range 
    ).idxmax(axis=0)

    #print(teste)

    temp1 = np.where(likelihood_r_t == 0, 1, likelihood_r_t)
    temp2 = temp1.cumprod(axis=1)

    posteriors = np.where(likelihood_r_t == 0, 0, temp2)

    posteriors = posteriors / np.sum(posteriors, axis=0)
    #print(posteriors)

    columns = pd.Index(range(11, 11+posteriors.shape[1]), name='Semanas')
    posteriors = pd.DataFrame(
        data = posteriors,
        index = r_t_range,
        columns = columns)


#     ax = posteriors.plot(
#         title='Posterior $P(R_t|k)$',
#         xlim=(0,16),
#         figsize=(12,5)
#    )
#    ax.legend(title='Semanas')
#    ax.set_xlabel('$R_t$');

    most_likely_values = posteriors.idxmax(axis=0)
#   print(most_likely_values)
    #x = most_likely_values.tail(3).iloc[0]
    #print(x)


    data =\
    [
    [0, most_likely_values.tail(3).iloc[0]],
    [1, most_likely_values.tail(2).iloc[0]],
    [2, most_likely_values.tail(1).iloc[0]]
    ]

    x = np.array(data)[:,0].reshape(-1,1)
    y = np.array(data)[:,1].reshape(-1,1)

    to_predict_x= [3]
    to_predict_x= np.array(to_predict_x).reshape(-1,1)

    regsr=LinearRegression()
    regsr.fit(x,y)
    predicted_y= regsr.predict(to_predict_x)
    m= regsr.coef_
    c= regsr.intercept_
    
    #print(predicted_y)
    
    return most_likely_values
    #print("Predicted y:\n",predicted_y)
    #print("slope (m): ",m)
    #print("y-intercept (c): ",c)


# @cache.memoize(timeout=timeout)  # in seconds
# def ACUM_TEMPORAL(lista_conf_se, SEs, last_se):

#     acum_temporal = []

#     for k in range (1, len(lista_conf_se)+1,1):
#         acum_temporal.append(lista_conf_se[0:k])
        

#     return acum_temporal

# @cache.memoize(timeout=timeout)  # in seconds
# def R0_TEMPORAL(acum_temporal):
    
#     r0_temporal = []

#     for k in range (1, len(acum_temporal)):
#         r0_temporal.append(round(calcula_r(acum_temporal[k]),2))
#     return r0_temporal

# Graphs

@cache.memoize(timeout=timeout)  # in seconds
def scatter1(df):
    dataStatus = df[['dataNotificacao','classificacaoFinal']]

    # Abaixo, as linhas com valores faltantes sao excluidas, o que implica em uma imprecisao dos
    # dados. Analisar formas de imputar tais datas

    dataStatus_ = dataStatus.dropna(axis=0)
    dataStatus_["value"]=1
    dataStatus_['dataNotificacao']=pd.to_datetime(dataStatus_['dataNotificacao'])
    dataStatus_=dataStatus_.loc[dataStatus_['classificacaoFinal']=="CONFIRMADO",:]

    situacao = dataStatus_.pivot_table(index='dataNotificacao', columns='classificacaoFinal', values="value", aggfunc='sum')\
                          .resample('d').sum()

    situacao["CONFIRMADO_ACUM"] = situacao["CONFIRMADO"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=situacao.index,
        y=situacao["CONFIRMADO_ACUM"],
        mode='lines+markers',
        hovertemplate = '<br><b>Data</b>: %{x}<br>'
                        '<br><b>Confirmados acumulados</b>: %{y}',
        name="Total acumulado de confirmados",
        line=dict(color='lightcoral')
        )
    )
    fig.add_trace(go.Scatter(
        x=situacao.index,
        y=situacao["CONFIRMADO"],
        mode='lines+markers',
        hovertemplate = '<br><b>Data</b>: %{x}<br>'
                        '<br><b>Confirmados/dia</b>: %{y}',
        name="Total de confirmados por dia",
        line=dict(color='royalblue'))
    )

    fig.update_layout(
        title={'text':'1 - Casos confirmados acumulados e novos casos por dia',
                'x':0.5,
                'yanchor': 'top'},
        xaxis_title="Data de notificação",
        yaxis_title="Confirmados",
        paper_bgcolor='#f5f5f5',
        legend = dict(y=0.8, 
                yanchor="bottom", 
                x=0.5, 
                xanchor="center"),
        margin={'t':50,'b':40,'l':20,'r':20})
    return fig

@cache.memoize(timeout=timeout)  # in seconds
def scatter2():

#	acum_temporal = ACUM_TEMPORAL(LISTA_CONF_SE(SEs, LAST_SE(SEs, situacao), situacao)[3:], SEs, LAST_SE(SEs, situacao))
#	io = LAST_SE(SEs, situacao) - len(R0_TEMPORAL(acum_temporal))
	# SEs_plot = [i for i in range(10, LAST_SE(SEs, situacao)-1)]

	fig = go.Figure()
	fig.add_trace(go.Scatter(
		x=list(calcula_r(LISTA_CONF_SE(SEs, LAST_SE(SEs, situacao), situacao)).index),
		y=calcula_r(LISTA_CONF_SE(SEs, LAST_SE(SEs, situacao), situacao)).values,
		mode='lines+markers',
		hovertemplate = '<br><b>SE</b>: %{x}<br>'
						'<br><b>R0</b>: %{y}',
		line=dict(color='crimson')
		)
	)
    
	fig.update_layout(
		title={'text':'Taxa de Contágio (R0) por Semana Epidemiológica (SE)',
				'x':0.5,
				'yanchor': 'top'},
		xaxis_title="SE",
		yaxis_title="R0",
		paper_bgcolor='#f5f5f5',
		legend = dict(y=0.8, 
				yanchor="bottom", 
				x=0.5, 
				xanchor="center"),
		margin={'t':50,'b':40,'l':20,'r':20})
		
	return fig

@cache.memoize(timeout=timeout)  # in seconds
def graf2(df):
	df = df[['dataNotificacao','municipio']].sort_values('dataNotificacao')
	df['count'] = 1
	table = pd.pivot_table(df, values='count', index='dataNotificacao', columns=['municipio'], aggfunc=np.sum).fillna(method='ffill')
	table2 = pd.melt(table.cumsum().reset_index(), id_vars=['dataNotificacao']).dropna()
	table2 = table2[table2['value']>1000]
	figure = px.line(table2, 
		x='dataNotificacao', 
		y='value', 
		color='municipio', 
		title="2 - Número de ocorrências por municipio",
		labels={
			'dataNotificacao':"Data de notificação"
		}).update_layout(yaxis_type="log",
			title={'x':0.5,
					'yanchor': 'top'},
			legend_title=None,
			yaxis_title="Ocorrências (log)",
			paper_bgcolor='#f5f5f5',
			margin={'t':50,'b':40,'l':20,'r':20},
			legend_orientation="h",
			showlegend=True,
			legend = dict(y=-0.3,
					x=0.5, 
					xanchor="center"))

	return figure

@cache.memoize(timeout=timeout)  # in seconds
def graf3(df):
	df = df.loc[(df['classificacaoFinal'] == 'CONFIRMADO')]

	ocorrMunicipios = []

	contagem = dict(df['municipio'].value_counts())
	ocorrMunicipios = contagem.keys()
	contagem_ = {}

	for municipio in MUNICIPIOS:
		formatedMun = MUN_DICT_G2D[municipio]
		if formatedMun in ocorrMunicipios:
			contagem_[municipio]=contagem[formatedMun]
		else:
			contagem_[municipio]=0

	escala = {}

	for municipio in contagem_.keys():
		if contagem_[municipio] == 0:
			escala[municipio] = '0'
		elif contagem_[municipio] in range(1,20):
			escala[municipio] = '1 a 20'
		elif contagem_[municipio] in range(20,100):
			escala[municipio] = '20 a 100'
		elif contagem_[municipio] in range(100,400):
			escala[municipio] = '100 a 400'
		elif contagem_[municipio] in range(400,1000):
			escala[municipio] = '400 a 1000'
		elif contagem_[municipio] in range(1000,2000):
			escala[municipio] = '1000 a 2000'
		elif contagem_[municipio] >= 2000:
			escala[municipio] = 'Mais de 2000'

	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations=MUNICIPIOS,
			hover_name=MUNICIPIOS,
			color=list(escala.values()),
			hover_data=[list(contagem_.values())],
			color_discrete_sequence= px.colors.sequential.Reds,
			category_orders={"color": ["0", "1 a 20", "20 a 100", "100 a 400", "400 a 1000","1000 a 2000", "Mais de 2000"]},
			mapbox_style="open-street-map",
			opacity=0.9,
			zoom=6,
			featureidkey='properties.name',
			center=dict(lat=-22.158536, lon=-42.684229),
			labels={'color':'Intervalo','hover_data_0':'Confirmados','locations':'Município'},
			range_color=(0,df['municipio'].value_counts().tolist()[0])
			).update_geos(fitbounds="locations",
			visible=False).update_layout(title={'text':'3 - Número de casos confirmados por município',
					'x':0.5,
					'yanchor': 'top'},
					paper_bgcolor='#f5f5f5',
					margin={'t':50,'b':40,'l':20,'r':20},
					legend_orientation="h")
	return fig

@cache.memoize(timeout=timeout)  # in seconds
def graf4(df):
	df = df.loc[(df['classificacaoFinal'] == 'CONFIRMADO') & (df['evolucaoCaso'] == 'OBITO')]

	ocorrMunicipios = []

	contagem = dict(df['municipio'].value_counts())
	ocorrMunicipios = contagem.keys()
	contagem_ = {}

	for municipio in MUNICIPIOS:
		formatedMun = MUN_DICT_G2D[municipio]
		if formatedMun in ocorrMunicipios:
			contagem_[municipio]=contagem[formatedMun]
		else:
			contagem_[municipio]=0

	escala = {}	

	for municipio in contagem_.keys():
		if contagem_[municipio] == 0:
		    escala[municipio] = '0'
		elif contagem_[municipio] in range(1,5):
		    escala[municipio] = '1 a 5'
		elif contagem_[municipio] in range(5,20):
		    escala[municipio] = '5 a 20'
		elif contagem_[municipio] in range(20,50):
		    escala[municipio] = '20 a 50'
		elif contagem_[municipio] in range(50,100):
		    escala[municipio] = '50 a 100'
		elif contagem_[municipio] >= 100:
		    escala[municipio] = 'Mais de 100'

	fig = px.choropleth_mapbox(df, geojson=RJ_MUN_GEOJSON, locations=MUNICIPIOS,
			hover_name=MUNICIPIOS,
			color=list(escala.values()),
			hover_data=[list(contagem_.values())],
			color_discrete_sequence= px.colors.sequential.Reds,
			category_orders={"color": ["0", "1 a 5", "5 a 20", "20 a 50", "50 a 100", "Mais de 100"]},
		mapbox_style="open-street-map",
		opacity=0.9,
		zoom=6,
		featureidkey='properties.name',
		center=dict(lat=-22.158536, lon=-42.684229),
		labels={'color':'Intervalo','hover_data_0':'Confirmados','locations':'Município'},
		range_color=(0,df['municipio'].value_counts().tolist()[0])
		).update_geos(fitbounds="locations",
		visible=False).update_layout(title={'text':'4 - Número de casos com óbito por município',
				'x':0.5,
				'yanchor': 'top'},
				paper_bgcolor='#f5f5f5',
				margin={'t':50,'b':40,'l':20,'r':20},
				legend_orientation="h")
	return fig	


@cache.memoize(timeout=timeout)  # in seconds
def graf5(df):
    df['idade'] = df['idade'].fillna(-1).astype(int)
    df = df.loc[(df['idade'] >= 0) & (df['classificacaoFinal'] == 'CONFIRMADO')]

    fig = go.Figure()

    fig.update_layout(yaxis=go.layout.YAxis(title='Idade'),
                    xaxis=go.layout.XAxis(
                        title='Número de Casos',
                        tickvals=[-200, -100, 0, 100, 200],
                        ticktext=[200,100,0,100,200]),
                    barmode='overlay',
                    title={'text':'5 - Número de casos confirmados por idade',
                                'x':0.5,
                                'yanchor': 'top'},
                        paper_bgcolor='#f5f5f5',
                        legend_orientation='h',
                        legend = dict(y=0.9, 
                                yanchor="bottom", 
                                x=0.5, 
                                xanchor="center"),
                        margin={'t':50,'b':40,'l':20,'r':20})

    fig.add_trace(go.Bar(y=df.loc[(df['sexo']=='M')]['idade'].value_counts().index,
                x=[x*-1 for x in df.loc[(df['sexo']=='M')]['idade'].value_counts()],
                orientation='h',
                opacity=.9,
                name='Homens',
                text=df.loc[(df['sexo']=='M')]['idade'].value_counts(),
                hoverinfo='text',
                marker=dict(color='royalblue')
                ))

    fig.add_trace(go.Bar(y=df.loc[(df['sexo']=='F')]['idade'].value_counts().index,
            x=df.loc[(df['sexo']=='F')]['idade'].value_counts(),
            orientation='h',
            opacity=.9,
            name='Mulheres',
            hoverinfo='x',
            marker=dict(color='crimson')
            ))


    return fig

@cache.memoize(timeout=timeout)  # in seconds
def graf6(df):
	df = df.loc[(df['classificacaoFinal'] == 'CONFIRMADO') & (df['evolucaoCaso'] == 'OBITO')]
	df['idade'] = df['idade'].fillna(-1).astype(int)
	df = df.loc[(df['idade'] >= 0)]

	fig = go.Figure()	

	fig.update_layout(yaxis=go.layout.YAxis(title='Idade'),
					xaxis=go.layout.XAxis(
						title='Número de Casos',
						tickvals=[-200, -100, 0, 100, 200],
						ticktext=[200,100,0,100,200]),
					barmode='overlay',
					title={'text':'6 - Número de óbitos por idade',
								'x':0.5,
								'yanchor': 'top'},
						paper_bgcolor='#f5f5f5',
						legend_orientation='h',
						legend = dict(y=0.9, 
								yanchor="bottom", 
								x=0.5, 
								xanchor="center"),
						margin={'t':50,'b':40,'l':20,'r':20})

	fig.add_trace(go.Bar(y=df.loc[(df['sexo']=='M')]['idade'].value_counts().index,
				x=[x*-1 for x in df.loc[(df['sexo']=='M')]['idade'].value_counts()],
				orientation='h',
				opacity=.9,
				name='Homens',
				text=df.loc[(df['sexo']=='M')]['idade'].value_counts(),
				hoverinfo='text',
				marker=dict(color='royalblue')
				))

	fig.add_trace(go.Bar(y=df.loc[(df['sexo']=='F')]['idade'].value_counts().index,
			x=df.loc[(df['sexo']=='F')]['idade'].value_counts(),
			orientation='h',
			opacity=.9,
			name='Mulheres',
			hoverinfo='x',
			marker=dict(color='crimson')
			))


	return fig
