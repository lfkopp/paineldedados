import sys
sys.path.append('./app')

from app.dashboard import app
from app.config import server

if __name__ == '__main__':
    app.run_server(debug=True)