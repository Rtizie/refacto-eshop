from flask import Flask,render_template
import sass

app = Flask(__name__)

sass.compile(dirname=('app/static/scss', 'app/static/css'))


@app.route("/")
def home_view():
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        return render_template('index.html')

@app.route("/kolekce")
def kolekce():
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        return render_template('kolekce.html')