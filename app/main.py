from datetime import timedelta
from flask import Flask,render_template,request,session
from flask.helpers import url_for
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
import logging
import sass
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clothes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = b'\xc36@\xa8\x80\x0bWO\x04\xb7\xdc\xc8\xdd3\xa4\xa2\xe9\xaeV\x0bd\xf9\x98\xde'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
logging.getLogger('werkzeug').setLevel('ERROR')
db = SQLAlchemy(app)

class Shirt(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		image = db.Column(db.String(300),nullable=False)
		name = db.Column(db.String(40),unique=True, nullable=False)
		collection = db.Column(db.String(40),nullable=False)
		color = db.Column(db.String(100), nullable=False)
		size = db.Column(db.String(20), nullable=False)
		cost = db.Column(db.Integer, nullable=False)
		stock = db.Column(db.Integer, nullable=False)

		def __repr__(self) -> str:
			return f'ID: {self.id},Fotka:{self.image}, Name:{self.name}, Collection:{self.collection}, Color:{self.color}, Size:{self.size}, Cost:{self.cost}, Stock:{self.stock}'


def handle_cart():
	products = []
	grand_total = 0
	index = 0
	quantity_total = 0

	print(f"Košík ve funkci:{session.get('cart')}")

	for item in session.get('cart'):
		print(f"Specifický produkt: {item}")
		if session['cart'] is []:
			return [],0,0
		shirt = Shirt.query.filter_by(name=item['name']).first()

		quantity = int(item['quantity'])
		total = quantity * shirt.cost
		grand_total += total

		quantity_total += quantity

		products.append({'id': shirt.id,'image':shirt.image, 'name': shirt.name,'color': item['color'],'size': item['size'],'quantity': quantity, 'total': total, 'index': index})
		index += 1
	print(f"Všechny produkty: {products}")
	return products, grand_total, quantity_total




@app.errorhandler(404)
def page_not_found(error):
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
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
	shirtData = Shirt.query.filter_by(name=shirt,collection=collection).all()
	if shirtData != []:
		sizes = shirtData[0].size.split(',')
		colors = shirtData[0].color.split(',')
		return render_template('shirt_page.html',image=shirtData[0].image,name=shirtData[0].name,cost=shirtData[0].cost,lenSizes=len(sizes),sizes=sizes,colors=colors,lenColors=len(colors),stock=shirtData[0].stock)
	else:
		abort(404)

@app.route('/addItem',methods=['GET','POST'])
def addItem():
	if request.method == 'POST':
		try:
			color = request.form.get('color')
			name = request.form.get('name')
			size = request.form.get('size')
			count = request.form.get('count')	
			shirtData = Shirt.query.filter_by(name=name).all()
			if shirtData != []:
				if 'cart' not in session:
					session['cart'] = []
				session['cart'].append({'name': name, 'quantity': count,'size': size,'color':color})
				print(f"Košík po přidání {session.get('cart')}")
		except Exception as e:
			raise e
	return redirect(url_for('cart'))

@app.route('/kosik')
def cart():
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	try:
		products, grand_total, quantity_total = handle_cart()
		return render_template('cart.html',items=products,grand_total=grand_total,quantity_total=quantity_total)
	except:
		return render_template('empty_cart.html',)

@app.route('/kolekce/<collection>')
def open_collection(collection):
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	try:
		shirts = Shirt.query.filter_by(collection=collection).all()
		return render_template('open_collection.html',title=collection,shirts=shirts)
	except Exception as e:
		raise(e)


