
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

# Pass user object to all Pages to achieve session
@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

#index#
@app.route('/')
def index():
    login_flag = request.args.get('login', 0)  
    return render_template('index.html', login=int(login_flag))

#MainProduct#
@app.route('/productMain', methods=['GET', 'POST'])
def product_main():
  
    user_id = session.get('user_id')
    

    if user_id:
        items = Item.query.filter(Item.user_id != user_id).all()
    else:
        items = Item.query.all()
    
    categories = []

    for item in items:
        category = item.category_id  
        if category == 1:
            categories.append('women')
        elif category == 2:
            categories.append('men')
        elif category == 3:
            categories.append('kids')

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        item = Item.query.get(item_id)
        
        if item:
            current_user = get_current_user()
            if current_user:
                user_id = current_user.id
                newItemCart = Cart(item_id=item_id, user_id=user_id, total_payment=item.price)
                db.session.add(newItemCart)
                db.session.commit()
                return redirect(url_for('cart'))

    return render_template('productMain.html', items=items, categories=categories)

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

      
        flash('Your message has been sent successfully!')
        print('Flash message set')
        return redirect(url_for('contact'))

    return render_template('contact.html')

#Cart#


@app.route('/shop-cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        if 'delete_item_id' in request.form:
            item_id = int(request.form['delete_item_id'])
            user_id = session.get('user_id')
            
            if user_id:
                # Delete the item from the cart
                Cart.query.filter_by(user_id=user_id, item_id=item_id).delete()
                db.session.commit()
                flash('Item deleted from cart successfully!')
            else:
                flash('You need to log in to delete items from your cart.')
            
            return redirect(url_for('cart'))
        
    user_id = session.get('user_id')
    if user_id:  
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        if not cart_items:
            flash('Your Cart is Empty')
            return render_template('shop-cart.html', items=[])
        item_ids = [item.item_id for item in cart_items]
    
        items = Item.query.filter(Item.id.in_(item_ids)).all()
    else:
        flash('You need to log in to view your cart.')
        return redirect(url_for('login'))

    return render_template('shop-cart.html', items=items)

#All published items
@app.route('/All_Published', methods=['GET', 'POST'])
def published():
    if request.method == 'POST':
      
        if 'delete_item_id' in request.form:
            item_id = int(request.form['delete_item_id'])
            
          
            Cart.query.filter_by(item_id=item_id).delete()
            db.session.commit()

            
            item = Item.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                flash('Item deleted successfully!')
            else:
                flash('Item not found!')
            return redirect(url_for('published'))

    user_id = session.get('user_id')
    items = Item.query.filter_by(user_id=user_id).all()
    if not items:
        flash('You have nothing to sell ')

    return render_template('All_Published.html', items=items)

#Update published products
@app.route('/UpdateProduct/<int:item_id>', methods=['GET', 'POST'])
def update_product(item_id):
    item = Item.query.get(item_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        item.name = name
        item.description = description
        item.price = price
        db.session.commit()
        flash('Product details updated successfully!')
        return redirect(url_for('published'))

    return render_template('UpdateProduct.html', item=item)
#Checkout#
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Successful login, set user ID in session
            session['user_id'] = user.id
            return redirect(url_for('index'))  
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

        user_id = session.get('user_id')
        rate =int(request.form.get('rating')) + 1

        image = request.form.get(f'imageUpload0')

        newItem = Item(name=title, description= discription, price=price, image= image, quantity=1, rate=rate, category_id=int(type), user_id=user_id )
 
        db.session.add(newItem)
        db.session.commit()

        # [show message ]
        flash('Your item has been added successfully!')
        print('Flash message set')
        return redirect(url_for('Additemtosell'))

    return render_template('Sellitem.html')


#Function for getting the categry from the item id
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
