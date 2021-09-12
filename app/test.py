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
