from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicial():
    return "servidor funcionando"

if __name__ == '__main__':
    app.run()
