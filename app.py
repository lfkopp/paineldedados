from flask import Flask,render_template,session,request,flash,redirect, url_for

app = Flask(__name__)
app.secret_key = "meuSegred0"

@app.route("/")
def home():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5000)
