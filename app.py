
###########################
#importing:
###########################

from flask import Flask, render_template, url_for, redirect , request , flash, session, jsonify
from models import db, User
from werkzeug.security import check_password_hash
from config import Config
from models import ContactMessage, User, Item, Category,Order,Review,Message,Cart
from sqlalchemy.exc import IntegrityError

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

# Function to get the current user object based on the user ID stored in the session
def get_current_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return User.query.get(user_id)
    return None  # Return None if no user is logged in

# Pass user object to all templates using context processor
@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

#index#
@app.route('/')
def index():
    login_flag = request.args.get('login', 0)  
    return render_template('index.html', login=int(login_flag))

#MainProduct#
@app.route('/productMain', methods=['GET'])
def product_main():
   

    items= Item.query.all()
    categories = []

    for item in items:
        category = item.category_id  
        if(category==1):
            categories.append('women')
        elif(category==2):
            categories.append('men')
        elif(category==3):
            categories.append('kids')
   
        
    return render_template('productMain.html',items=items, categories=categories)

#Contact#
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
        # Get the current user ID from the session
        user_id = session.get('user_id')

        if user_id:
            # Retrieve items in the cart for the current user
            items = Item.query.filter_by(user_id=user_id).all()
            if not items:
                flash('Your Cart is Empty')
        else:
            flash('You need to log in to view your cart.')
            return redirect(url_for('login'))

    elif request.method=='POST':
        # Process POST request for adding items to the cart
        if request.form['form_name'] == 'form1':
            quantity = request.form.get('quantity')

    return render_template('shop-cart.html', items=items)

#Checkout#
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Successful login, set user ID in session
            session['user_id'] = user.id
            return redirect(url_for('index'))  # Redirect to index after successful login
        else:
            # Invalid credentials
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    
    session.pop('user_id', None)
    return redirect(url_for('index'))
#Profile

@app.route('/Profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Extract form data
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        # Update user's information in the database
        current_user = get_current_user()
        try:
            current_user.username = new_username
            current_user.password = new_password
            db.session.commit()
            flash('Your data has been Updated successfully!')
            print('Flash message set')
            return redirect(url_for('profile'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Username already exists. Please choose a different username.')
             
            print('Flash message set')
            return redirect(url_for('profile'))
    
    return render_template('Profile.html')

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

        return render_template('index.html')

    return render_template('Register.html')




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

        image = request.form.get(f'imageUpload0')

            

        newItem = Item(name=title, description= discription, price=price, image= image, quantity=1, rate=rate, category_id=int(type), user_id=1 )
 
        db.session.add(newItem)
        db.session.commit()

        # [show message ]
        flash('Your item has been added successfully!')
        print('Flash message set')
        return redirect(url_for('Additemtosell'))

    return render_template('Sellitem.html')

@app.route('/productMain', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        item_id = request.form.get('itemnumber')
        item = Item.query.filter_by(id=item_id).first()
        current_user = get_current_user()
        
        if current_user:
            user_id = current_user.id
            newItemCart = Cart(item_id=item_id, user_id=user_id, total_payment=item.price)
            db.session.add(newItemCart)
            db.session.commit()
            return redirect(url_for('cart'))
        else:
            flash('Please log in to add items to your cart.')
            return redirect(url_for('login'))
        
    return render_template('productMain.html')
def get_category_name(category_id):
    if category_id == 1:
        return 'Women'
    elif category_id == 2:
        return 'Men'
    elif category_id == 3:
        return 'Kids'
    else:
        return 'Other'
#Search
@app.route('/basic',methods=['POST'])
def search():
    query = request.form.get('query', '').strip()
    if query:
        items = Item.query.filter(
            (Item.name.ilike(f'%{query}%')) |
            (Item.description.ilike(f'%{query}%'))
        ).all()
       
        if items:
            categories = [get_category_name(item.category_id) for item in items]
            return render_template('search_results.html', items=items, categories=categories, query=query)
        else:
            flash('No results found for "{}"'.format(query))
            return render_template('search_results.html')
        return redirect(request.referrer or url_for('index'))


###########################
#running the application:
###########################

if __name__ == "__main__": #run the application dynamically
    app.run(debug=True) #to run in debug mode
