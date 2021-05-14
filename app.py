from flask import Flask,render_template,session,request,flash,redirect, url_for

app = Flask(__name__)
app.secret_key = "meuSegred0"

@app.route("/")
def home():
    return render_template('main.html')

@app.route("/financas")
def fincancas():
    return render_template('financas.html')

@app.route("/educacao")
def educacao():
    return render_template('educacao.html')

@app.route("/saude")
def saude():
    return render_template('saude.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)
