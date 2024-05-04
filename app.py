from flask import Flask, render_template, url_for, redirect , request , flash
from models import db, User
from config import Config
from models import ContactMessage
app = Flask(__name__)
#remeber to make it hidden on pupblic [important]
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        contact_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(contact_message)
        db.session.commit()

        # [show message ]
        flash('Your message has been sent successfully!')
        print('Flash message set')
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/shop-cart')
def cart():
    return render_template('shop-cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
if __name__ == "__main__":
    app.run(debug=True)
