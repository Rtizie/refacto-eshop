from re import S
from flask import Flask,render_template
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy

import sass

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clothes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = b'\xc36@\xa8\x80\x0bWO\x04\xb7\xdc\xc8\xdd3\xa4\xa2\xe9\xaeV\x0bd\xf9\x98\xde'

db = SQLAlchemy(app)

class Shirt(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(40),unique=True, nullable=False)
        collection = db.Column(db.String(40),nullable=False)
        color = db.Column(db.String(100), nullable=False)
        size = db.Column(db.String(20), nullable=False)
        cost = db.Column(db.Integer, nullable=False)
        stock = db.Column(db.Integer, nullable=False)

        def __repr__(self) -> str:
            return f'ID: {self.id}, Name:{self.name}, Collection:{self.collection}, Color:{self.color}, Size:{self.size}, Cost:{self.cost}, Stock:{self.stock}'


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404


@app.route("/")
def home_view():
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        return render_template('index.html')

@app.route("/kolekce")
def kolekce():
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        return render_template('kolekce.html')

@app.route("/database")
def testPage():
        return render_template('data.html',var=Shirt.query.all()[0].cost)

@app.route("/kolekce/<collection>/<shirt>")
def openShirt(collection,shirt):
        sass.compile(dirname=('app/static/scss', 'app/static/css'))
        shirtData = Shirt.query.filter_by(name=shirt).all()
        if shirtData != []:
                sizes = shirtData[0].size.split(',')
                colors = shirtData[0].color.split(',')
                return render_template('shirt_page.html',name=shirtData[0].name,cost=shirtData[0].cost,lenSizes=len(sizes),sizes=sizes,colors=colors,lenColors=len(colors),stock=shirtData[0].stock)
        else:
                abort(404)

@app.route("/test")
def test():
        return render_template('test.html')