from flask import Flask,render_template
import sass

app = Flask(__name__)

from app.data.data import *

sass.compile(dirname=('app/static/scss', 'app/static/css'))


@app.route("/")
def home_view():
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        return render_template('index.html')

@app.route("/kolekce")
def kolekce():
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        return render_template('kolekce.html')

@app.route("/test")
def testPage():
        data = getData()
        return render_template('test.html', var=data['shirts']['kekw'][0]['size'])