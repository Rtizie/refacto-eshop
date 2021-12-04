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
#logging.getLogger('werkzeug').setLevel('ERROR')
db = SQLAlchemy(app)

class Shirt(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		image = db.Column(db.String(300),nullable=False)
		imageCart = db.Column(db.String(300),nullable=False)
		name = db.Column(db.String(40),unique=True, nullable=False)
		description = db.Column(db.String(600),nullable=False)
		collection = db.Column(db.String(40),nullable=False)
		color = db.Column(db.String(100), nullable=False)
		size = db.Column(db.String(20), nullable=False)
		cost = db.Column(db.String(5), nullable=False)
		stock = db.Column(db.String(10), nullable=False)

		def __repr__(self) -> str:
			return f'ID: {self.id},Fotka:{self.image},Fotka v Košíku:{self.imageCart}, Name:{self.name}, Collection:{self.collection}, Color:{self.color}, Size:{self.size}, Cost:{self.cost}, Stock:{self.stock}'


def handle_cart(cart):
	products = []
	grand_total = 0
	index = 0
	quantity_total = 0

	for item in cart:
		if session['cart'] is []:
			return [],0,0
		shirt = Shirt.query.filter_by(name=item['name']).first()

		quantity = int(item['quantity'])
		total = quantity * int(shirt.cost)
		grand_total += total

		quantity_total += quantity

		products.append({'id': shirt.id,'image':shirt.image,'imageCart':shirt.imageCart, 'name': shirt.name,'color': item['color'],'size': item['size'],'quantity': quantity, 'total': total, 'index': index})
		index += 1
	return products, grand_total, quantity_total


@app.route("/cart_remove",methods=['GET','POST'])
def cart_remove():
	ID = request.form.get('id')
	name = request.form.get('name')
	color = request.form.get('color')
	quantity = request.form.get('quantity')
	size = request.form.get('size')
	cart = session.get('cart')
	
	for count,item in enumerate(cart):
		print(item)
		print(ID)
		if item['id'] == ID:
			if item['name'] == name:
				if item['color'] == color:
					if item['quantity'] == quantity:
						if item['size'] == size:
							del cart[count]
	session.update()
	return redirect(url_for('cart'))


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

@app.route("/kontakt")
def contact():
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template('contact.html', title="Kontakt")

@app.route("/kolekce/<collection>/<shirt>")
def openShirt(collection,shirt):
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	shirtData = Shirt.query.filter_by(name=shirt,collection=collection).all()
	if shirtData != []:
		sizes = shirtData[0].size.split(',')
		colors = shirtData[0].color.split(',')
		return render_template('shirt_page.html',id=shirtData[0].id,image=shirtData[0].image,name=shirtData[0].name,cost=shirtData[0].cost,lenSizes=len(sizes),sizes=sizes,colors=colors,lenColors=len(colors),stock=shirtData[0].stock)
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
			id = request.form.get('id')
			skip = False

			#Bere Databázi	
			shirtData = Shirt.query.filter_by(name=name).all()
			if shirtData != []:
				if 'cart' not in session:
					print("Vytvořený cart")
					session['cart'] = []
				try:
					for countL,item in enumerate(session.get('cart')):
						if item["name"] != name or item["color"] != color or item["size"] != size:
							continue
						else:
							session.get('cart')[countL]["quantity"] = str(int(session.get('cart')[countL]["quantity"]) + int(item["quantity"]))
							skip = True
							break
					if skip is not True:		
						session['cart'].append({'id': id,'name': name, 'quantity': count,'size': size,'color':color})
				except Exception as e:
					raise(e)
				session.update()
		except Exception as e:
			raise e
	return redirect(url_for('cart'))

@app.route('/kosik')
def cart():
	cart = session.get('cart')
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	try:
		products, grand_total, quantity_total = handle_cart(cart)
		if grand_total == 0:
			return render_template('empty_cart.html',)
		return render_template('cart.html',items=products,grand_total=grand_total,quantity_total=quantity_total)
	except Exception as e:
		print(e)
		return render_template('empty_cart.html',)

@app.route('/kolekce/<collection>')
def open_collection(collection):
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	try:
		shirts = Shirt.query.filter_by(collection=collection).all()
		return render_template('open_collection.html',title=collection,shirts=shirts)
	except Exception as e:
		raise(e)


