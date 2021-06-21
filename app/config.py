# Imports
import dash
import flask
from flask_caching import Cache
import os

# Supress Pandas Warnings
import warnings
warnings.filterwarnings("ignore")



# App & Server settings
server = flask.Flask(__name__)
app = dash.Dash(
	__name__,
    #meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    server=server,
    url_base_pathname='/'
)

app.title = "Painel de Dados das Cidades - Rio de Janeiro"

# Cache settings
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

timeout = 60

@server.route('/update')
def update():
    os.system('. ~/web/update.sh')
    return "<h1>Atualizando!</h1><br><a href='/'>Voltar para o Dashboard</a>"