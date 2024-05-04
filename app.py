from flask import Flask, render_template, url_for, redirect , request , flash
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productMain')
def product_main():
    return render_template('productMain.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/shop-cart')
def cart():
    return render_template('shop-cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
if __name__ == "__main__":
    app.run(debug=True)
