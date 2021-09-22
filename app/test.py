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
