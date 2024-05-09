from flask import Flask, render_template, url_for, redirect , request , flash, session
from models import db, User
from config import Config
from models import ContactMessage, User, Item, Category,Order,Review,Message,Cart

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


@app.route('/shop-cart',methods=['GET','POST'])
def cart():
    if request.method=='GET':
         #get items that user put in cart using query(need user id and search in orders (wtd for guest?))
         #get the items in an array and pass the array to html
         #loop through the array and extract name, img, price,..etc
         #make the buttons interactive
         #if user put address, i fguest let him put address
         #add shipping cost then you'd have the order details 
       #  userID=User.query.filter_by()
        #quantity=request.data
        userID=1 #we'll be getting user id from login or guest session
        items=Item.query.filter_by(user_id=userID) # currently getting all items untill user login/guest
        if items.count==0:
            flash('Your Cart is Empty')
    elif request.method=='POST':

        if request.form['form_name'] == 'form1':
            quantity=request.form.get('quantity')
    return render_template('shop-cart.html', items=items)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
if __name__ == "__main__":
    app.run(debug=True)
