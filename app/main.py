from datetime import timedelta
from flask import Flask,render_template,request,session,Response
from flask.helpers import url_for
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
import logging
import sass
from werkzeug.utils import redirect
from email.mime.text import MIMEText
from functools import wraps


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clothes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = b'\xc36@\xa8\x80\x0bWO\x04\xb7\xdc\xc8\xdd3\xa4\xa2\xe9\xaeV\x0bd\xf9\x98\xde'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
#logging.getLogger('werkzeug').setLevel('ERROR')
db = SQLAlchemy(app)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

class Shirt(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		display_image = db.Column(db.String(300),nullable=False)
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

class Order(db.Model):
		orderId = db.Column(db.Integer, primary_key=True)
		firstName = db.Column(db.String(64),nullable=False)
		lastName = db.Column(db.String(64),nullable=False)
		email = db.Column(db.String(128), nullable=False)
		town = db.Column(db.String(64),nullable=False)
		delivery = db.Column(db.String(64),nullable=False)
		phone = db.Column(db.String(128), nullable=False)
		products = db.Column(db.String(800), nullable=False)
		payment = db.Column(db.String(16), nullable=False)
		address = db.Column(db.String(64), nullable=False)
		psc = db.Column(db.String(64), nullable=False)
		
		def __init__(self,firstName,lastName,email,town,delivery,phone,products,payment,address,psc) -> None:
			self.firstName = firstName
			self.lastName = lastName
			self.email = email
			self.town = town
			self.delivery = delivery
			self.phone = phone
			self.products = products
			self.payment = payment
			self.address = address
			self.psc = psc
			

		def __repr__(self) -> str:
			return f'{self.orderId},{self.firstName},{self.lastName},{self.email},{self.town},{self.delivery},{self.phone},{self.products},{self.payment},{self.address},{self.psc}'



def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	return username == 'rtizie' and password == 'refactoIT2023Objednavky'

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated


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


@app.route("/kosik/checkout")
def checkout():
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template("checkout.html",number_of_items_in_basket=len(session.get('cart')))

@app.route('/kosik/checkout/platba',methods=['POST'])
def payment():
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	firstName = request.form.get('first')
	lastName = request.form.get('last')
	email = request.form.get('email')
	phone = request.form.get('phone')
	address = request.form.get('address')
	psc = request.form.get('psc')
	town = request.form.get('town')
	delivery = request.form.get('delivery')
	print(f"{firstName},{lastName},{email},{phone},{address},{psc},{town},{delivery}")
	cart = session.get('cart')
	products, grand_total, quantity_total = handle_cart(cart)
	if delivery == 'zasilkovna':
		deliveryC = 69
	elif delivery == 'posta':
		deliveryC = 109
	elif delivery == 'ppl':
		deliveryC = 99
	elif delivery == 'local':
		deliveryC = 0
	delivery_total = grand_total + deliveryC
	print(delivery_total)
	
	return render_template('payment.html',products=products,grand_total=grand_total,delivery=deliveryC,delivery_total=delivery_total,firstName=firstName,lastName=lastName,email=email,phone=phone,address=address,town=town,psc=psc,deliveryV=delivery,number_of_items_in_basket=len(session.get('cart')))


@app.route("/platbaOK")
def paymentOK():
	session['cart'] = []
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template('paymentOK.html',number_of_items_in_basket=len(session.get('cart')))

@app.route("/kekw")
@requires_auth
def objednavky():
	data = Order.query.all()
	return render_template('objednavky.html',data=data)



@app.errorhandler(404)
def page_not_found(error):
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []	
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template('404.html',number_of_items_in_basket=len(session.get('cart'))), 404


@app.route("/")
def home_view():
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []	
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template('index.html',number_of_items_in_basket=len(session.get('cart')))

@app.route("/kolekce")
def kolekce():
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []	
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template('kolekce.html',number_of_items_in_basket=len(session.get('cart')))

@app.route("/kontakt")
def contact():
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	return render_template('contact.html', title="Kontakt",number_of_items_in_basket=len(session.get('cart')))

@app.route("/kolekce/<collection>/<shirt>")
def openShirt(collection,shirt):
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	shirtData = Shirt.query.filter_by(name=shirt,collection=collection).all()
	if shirtData != []:
		images = shirtData[0].image.split(',')
		sizes = shirtData[0].size.split(',')
		colors = shirtData[0].color.split(',')
		return render_template('shirt_page.html',number_of_items_in_basket=len(session.get('cart')),id=shirtData[0].id,images=images, lenImages=len(images),description=shirtData[0].description,name=shirtData[0].name,cost=shirtData[0].cost,lenSizes=len(sizes),sizes=sizes,colors=colors,lenColors=len(colors),stock=shirtData[0].stock)
	else:
		abort(404)



@app.route('/kosik')
def cart():
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []	
	cart = session.get('cart')
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	try:
		products, grand_total, quantity_total = handle_cart(cart)
		if grand_total == 0:
			return render_template('empty_cart.html',number_of_items_in_basket=len(session.get('cart')))
		return render_template('cart.html',items=products,grand_total=grand_total,quantity_total=quantity_total,number_of_items_in_basket=len(session.get('cart')))
	except Exception as e:
		print(e)
		return render_template('empty_cart.html',number_of_items_in_basket=len(session.get('cart')))

@app.route('/kolekce/<collection>')
def open_collection(collection):
	if 'cart' not in session:
		print("Vytvořený cart")
		session['cart'] = []	
	sass.compile(dirname=('app/static/scss', 'app/static/css'))
	try:
		shirts = Shirt.query.filter_by(collection=collection).all()
		return render_template('open_collection.html',title=collection,shirts=shirts,number_of_items_in_basket=len(session.get('cart')))
	except Exception as e:
		raise(e)


"""
	API
"""

#Custom Desing Pages

from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
class CustomDesing(FlaskForm):
	email = StringField('E-Mail', validators=[DataRequired()])
	image = FileField('Image File', validators=[FileRequired()])
	notes = TextAreaField('')


@app.route('/custom_desing_add',methods=['POST'])
def custom_desing_add():
	try:
		email = request.form.get('email')
		photo = request.files.get('image')
		photo.filename = email
		photo.save(f"app/static/custom_desing/{email}.png")
		return redirect('/vlastni-navrh-ok')
	except Exception as e:
		print(e)
		return redirect('/vlastni-navrh-error')
	

@app.route("/cart_remove",methods=['POST'])
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
	return redirect(url_for('cart',number_of_items_in_basket=len(session.get('cart'))))


@app.route('/addItem',methods=['POST'])
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
	return redirect(url_for('cart',number_of_items_in_basket=len(session.get('cart'))))


@app.route('/kosik/checkout/data',methods=['POST'])
def data():
	try:
		data = request.get_json()
		print(data)
		firstName = data['firstName']
		lastName = data['lastName']
		town = data['town']
		psc = data['psc']
		delivery = data['delivery']
		email = data['email']
		phone = data['phone']
		products = str(session.get('cart'))
		productsB = MIMEText(products,'plain','utf-8')
		payment = data['cost']
		address = data['address']
		order = Order(firstName=firstName,lastName=lastName,town=town,psc=psc,delivery=delivery,email=email,phone=phone,products=productsB.as_string(),payment=payment,address=address)
		db.session.add(order)
		db.session.commit()
		return "Success"
	except Exception as e:
		print(e)
		raise e
