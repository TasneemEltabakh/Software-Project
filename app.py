
###########################
#importing:
###########################

from flask import Flask, render_template, url_for, redirect , request , flash, session, jsonify
from models import db, User
import uuid
from config import Config
from models import ContactMessage, User, Item, Category,Order,Review,Message,Cart


app = Flask(__name__)
#remeber to make it hidden on pupblic [important]
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Secret key for session encryption
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

###########################
#Pages:
###########################

#index#
@app.route('/')
def index():
    # Check if session ID exists, generate one if not
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Generate unique session ID
    return render_template('index.html')

#MainProduct#
@app.route('/productMain')
def product_main():
    return render_template('productMain.html')
<<<<<<< HEAD

#Login#
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Successful login
            return 'Login successful'
        else:
            # Invalid credentials
            return 'Invalid credentials'

    return render_template('Login.html')

#Register#
@app.route('/Register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        phone_number = request.form['number']
        username = request.form['username']
        address = request.form['address']

        user = User(email=email, password=password, phone_number=phone_number, username=username, address=address)
        db.session.add(user)
        db.session.commit()

        #return redirect(url_for('login'))
        return render_template('index.html')

    return render_template('Register.html')


#Contact#
=======
 
>>>>>>> 0ab81a9b5c4c7e54b238277860d42d9c5580ebb6
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

#Cart#
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

#Checkout#
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

#Login#
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Successful login
            return 'Login successful'
        else:
            # Invalid credentials
            return 'Invalid credentials'

    return render_template('Login.html')

#Register#
@app.route('/Register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        phone_number = request.form['number']
        username = request.form['username']
        address = request.form['address']

        user = User(email=email, password=password, phone_number=phone_number, username=username, address=address)
        db.session.add(user)
        db.session.commit()

        #return redirect(url_for('login'))
        return render_template('index.html')

    return render_template('Register.html')


#Contact#
#Sell New Item#
@app.route('/Sellitem', methods=['GET', 'POST'])
def Additemtosell():
    if request.method == 'POST':
        title = request.form.get('title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        type = request.form.get('type')
        discription = request.form.get('description')
        location = request.form.get('location')
        status = request.form.get('itemStatus')
        priceType = int(request.form.get('priceType'))  
        if(priceType==0):
            price = 0
        else:
            price = request.form.get('priceInput')
         
        rate = request.form.get('rating')
        image = request.form.get('imageUpload0')
        newItem = Item(name=title, description= discription, price=price, image= image, quantity=1, rate=rate, category_id=int(type), user_id=1 )
 
        db.session.add(newItem)
        db.session.commit()

        # [show message ]
        flash('Your item has been added successfully!')
        print('Flash message set')
        return redirect(url_for('Additemtosell'))

    return render_template('Sellitem.html')

###########################
#running the application:
###########################

if __name__ == "__main__": #run the application dynamically
    app.run(debug=True) #to run in debug mode
