# Imports
import dash
import flask
from flask_caching import Cache


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

app.title = "Painel de Gestão Local - Rio de Janeiro"

# Cache settings
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

timeout = 60

