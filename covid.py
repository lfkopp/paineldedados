#%%
## fonte: http://sistemas.saude.rj.gov.br/tabnetbd/webtabx.exe?Linha=Regi%E3o+de+Sa%FAde%2FMunic%EDpio%7C%27%26%27%2Bdbo.td_municipio.co_reg_saude%2B%27+%27%2Bdbo.td_municipio.no_reg_saude+_subtotal_+no_municipio+where+codmun+%3D+dbo.td_municipio.co_municipio&Coluna=--N%E3o-Ativa--&Incremento=Casos%7Ccasos_dia&Incremento=%D3bitos%7Cobitos_dia&Incremento=Casos++por+100.000+habitantes%7C%3Dcase+when+sum%28pop2019%29+%3E+0+then+sum%28casos_dia*100000%29%2Fsum%28pop2019%29+else+0+end%7C1&Incremento=Graf+Casos++por+100.000+habitantes%7C%3Dcase+when+sum%28pop2019%29+%3E+0+then+sum%28casos_dia*100000%29%2Fsum%28pop2019%29+else+0+end%7C1%7CBarFormat%28%7Bwidth%3A+200%2C+showValue%3A+false%7D%29&Incremento=%D3bitos+por+100.000+habitantes%7C%3Dcase+when+sum%28pop2019%29+%3E+0+then+sum%28obitos_dia*100000%29%2Fsum%28pop2019%29+else+0+end%7C1&Incremento=Gr%E1f+%D3bitos+por+100.000+habitantes%7C%3Dcase+when+sum%28pop2019%29+%3E+0+then+sum%28obitos_dia*100000%29%2Fsum%28pop2019%29+else+0+end%7C1%7CBarFormat%28%7Bwidth%3A+200%2C+showValue%3A+false%7D%29&Incremento=Popula%E7%E3o+2019%7C%3Dsum%28pop2019%29&Incremento=Letalidade%7C%3Dcase+when+sum%28casos_dia%29+%3E+0+then+sum%28obitos_dia%29*100.0+%2F+sum%28casos_dia%29+else+0+end%7C1&nomedef=covid19%2Fcovid_munic_diarioh.def&grafico=
import pandas as pd
from app.functions import remover_acentos
# %%
df = pd.read_csv('http://sistemas.saude.rj.gov.br/tabnetbd/csv/covid_munic_diarioh16280158591.csv',decimal=',', sep=';', encoding='latin-1', usecols=['Região de Saúde/Município','Casos','Óbitos','Casos  por 100.000 habitantes','Óbitos por 100.000 habitantes',"População 2019"])
df.columns = ['municipio','casos','obitos','casopor100k','obitopor100k','pop']
df = df[df['municipio'].str.startswith('.')]
df['municipio'] = df['municipio'].str.replace('.', '').str.upper()
df['municipio'] = df['municipio'].apply(remover_acentos)

# %%
finbra = pd.read_csv('app/data/finbra_desp.csv', sep=';', decimal='.', usecols=['municipio','ano','10 - Saúde'])
finbra.columns = ['municipio','ano','saude']
finbra = finbra[finbra['ano'] >= 2019]
finbra
# %%
df2 = df.merge(finbra, on='municipio')
df2['letalidade'] = df2.obitos / df2.casos
df2['saudepop'] = df2['saude'] / df2['pop']
# %%
df2 = df2.sort_values('municipio')
df2.to_csv('app/data/saude.csv', index=False)
# %%
#import plotly.express as px
# %%
#px.scatter(df2, x='saudepop', y='letalidade', color="municipio", trendline="ols", hover_data=['municipio','casos','obitos'], title="Graf. 1 - Letalidade x Gasto de saúde per capita")
from unicodedata import normalize

def remover_acentos(txt):
	return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

NUPEC = ['Areal','Armação dos Búzios','Casimiro de Abreu','Comendador Levy Gasparian','Iguaba Grande','Miguel Pereira','Paraíba do Sul','Quissamã','Rio Claro','Rio das Flores','São Pedro da Aldeia', 'Sapucaia','Saquarema','Três Rios']

CENTRO = ['Paty do Alferes','Vassouras','Mendes','Barra do Piraí','Engenheiro Paulo de Frontin','Piraí','Paracambi','São José do Vale do Rio Preto','Valença','Areal','Comendador Levy Gasparian','Miguel Pereira','Paraíba do Sul','Rio Claro','Rio das Flores', 'Sapucaia','Três Rios']

NORTE = ['Conceição de Macabu','Rio Bonito','Silva Jardim','Rio das Ostras','Carapebus','Arraial do Cabo','Araruama','Cabo Frio','Armação dos Búzios','Casimiro de Abreu','Iguaba Grande','Quissamã','São Pedro da Aldeia','Saquarema']

grupos = {  'NUPEC': [remover_acentos(x) for x in NUPEC],
            'CENTRO': [remover_acentos(x) for x in CENTRO],
            'NORTE': [remover_acentos(x) for x in NORTE]}

def trata_local(local):
    if type(local) == str:
        local = [local]
    local = [remover_acentos(x) for x in local]
    local = list(set(local))
    for grupo in ['NUPEC', 'NORTE', 'CENTRO']:
        if grupo in local:
            local.remove(grupo)
            local = list(set(local + grupos[grupo]))
    local.sort()
    return local

# %%
trata_local(['nupéc','Rio de Janeiro'])
# %%
    
