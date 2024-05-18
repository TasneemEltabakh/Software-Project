#################################
#Importing required libraries
################################
from flask import Flask, render_template, url_for, redirect, request, flash, session
from models import db, User, PromoCode, ContactMessage, Item, Cart, Order, Subscription
from werkzeug.security import check_password_hash
from config import Config
from sqlalchemy.exc import IntegrityError
from datetime import datetime


###################################################
#Design Patterns templates 
###################################################
#1.Singlton 
app = Flask(__name__, static_url_path='/static', static_folder='static')#application instance.

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()


#2. Factory design Pattern

class ItemFactory:
    @staticmethod
    def create_item(name, description, price, image, quantity, rate, category_id, user_id):
        return Item(name=name, description=description, price=price, image=image, quantity=quantity, rate=rate, category_id=category_id, user_id=user_id)

class MessageFactory:
    @staticmethod
    def create_message(name, email, message):
        return ContactMessage(name=name, email=email, message=message)

#3. Strategy design Pattern

class CheckoutStrategy:
    def apply_strategy(self, total_price):
        raise NotImplementedError

class DefaultCheckoutStrategy(CheckoutStrategy):
    def apply_strategy(self, total_price):
        return total_price

class DiscountCheckoutStrategy(CheckoutStrategy):
    def __init__(self, discount_percentage):
        self.discount_percentage = discount_percentage

    def apply_strategy(self, total_price):
        # Calculate the discounted price
        discount_amount = total_price * (self.discount_percentage / 100)
        discounted_price = total_price - discount_amount
        return discounted_price

#################################
#Helping Functions
#################################
def get_current_user():
    if 'user_id' in session:
        user_id = session['user_id']
        return User.query.get(user_id)
    return None

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

def get_category_name(category_id):
    if category_id == 1:
        return 'women'
    elif category_id == 2:
        return 'men'
    elif category_id == 3:
        return 'kid'
    else:
        return 'Other'


####################################
#Pages
####################################

#index
@app.route('/')
def index():
    login_flag = request.args.get('login', 0)  
    return render_template('index.html', login=int(login_flag))

#MainProduct#
@app.route('/productMain', methods=['GET', 'POST'])
def product_main():

    #first, we see that if this user is logged in
    user_id = session.get('user_id')
    #get all numbers for the users who published products
    user_phone_numbers = {}
    if user_id:
        items = Item.query.filter(Item.user_id != user_id).all()
        for item in items:
            user = User.query.get(item.user_id)
            if user:
                user_phone_numbers[item.id] = user.phone_number
        
        
    else:
        items = Item.query.all()
    
    # this function for filtering in the front end  
    categories = []
    for item in items:
        category = item.category_id  
        if category == 1:
            categories.append('women')
        elif category == 2:
            categories.append('men')
        elif category == 3:
            categories.append('kids')
    
    #if add to cart
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

    return render_template('productMain.html', items=items, categories=categories,user_phone_numbers=user_phone_numbers)

#contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        contact_message = MessageFactory.create_message(name=name, email=email, message=message)
        db.session.add(contact_message)
        db.session.commit()
        flash('Your message has been sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')


#Cart#
@app.route('/shop-cart', methods=['GET', 'POST'])
def cart():
    session['promo_code'] = 0
    #if any button is pressed
    if request.method == 'POST':
        #if this button was for delete
        if 'delete_item_id' in request.form:
            #get the item id you want to delete and the user id for the person who wants to delete
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
        
        #if the button was applying the promocode
        elif 'promo_code' in request.form:
            #get the entered promocode
            promo_code = request.form.get('promo_code')
            promo = PromoCode.get_by_code(promo_code)
            #if this is a valid promocodes
            if promo:
                session['promo_code'] = promo.code
                flash('Promo code applied successfully!')
            else:
                flash('Invalid promo code. Please try again.', 'error')

    # Handle GET request as before
    user_id = session.get('user_id')
    if user_id:
        # this is for showing all the products you put in the cart  
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        cart_items_count = len(cart_items)
        #this item counts for the header icon
        session['cart_items_count'] = cart_items_count
        if not cart_items:
            flash('Your Cart is Empty')
            return render_template('shop-cart.html', items=[], total_price=0)
        item_ids = [item.item_id for item in cart_items]
    
        items = Item.query.filter(Item.id.in_(item_ids)).all()
       
        # Calculate total price of items in the cart
        total_price = sum(item.price for item in items)
        promo_code = session.get('promo_code')
        
        #if the promocode is valid, apply the discount
        if promo_code:
            promo = PromoCode.get_by_code(promo_code)
            if promo:
                discount_percentage = promo.discount_percentage
                discount = total_price * (discount_percentage / 100)
                total_price -= discount      

    else:
        flash('You need to log in to view your cart.')
        return redirect(url_for('login'))

    return render_template('shop-cart.html', items=items, total_price=total_price)


#All publish
@app.route('/All_Published', methods=['GET', 'POST'])
def published():
    if request.method == 'POST':
        
        #if the user who published the item wants to delete it
        if 'delete_item_id' in request.form:
            item_id = int(request.form['delete_item_id'])
            
            #it will be also deleted from the cart if any one puts it in
            Cart.query.filter_by(item_id=item_id).delete()
            db.session.commit()

            #then delete it itself
            item = Item.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                flash('Item deleted successfully!')
            else:
                flash('Item not found!')
            return redirect(url_for('published'))
        
    #after that, the items are updated to give the list without the deleted one 
    user_id = session.get('user_id')
    items = Item.query.filter_by(user_id=user_id).all()
    if not items:
        flash('You have nothing to sell ')

    return render_template('All_Published.html', items=items)


#Update published products by the selected id, so we passed the id to the backend 
@app.route('/UpdateProduct/<int:item_id>', methods=['GET', 'POST'])
def update_product(item_id):

    #getting all the data of the choosen id
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
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # get the user id to filter his cart contents to the checkout
    user_id = session.get('user_id')
    total_price_with_tax = float(request.args.get('total_price', 0))
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    items = []
    total_price = 0
    for cart_item in cart_items:
        item = Item.query.get(cart_item.item_id)
        items.append(item)
        
        # this is mainly for the required fields 
        if request.method == 'POST':
                required_fields = ['first_name', 'last_name', 'country', 'address', 'city', 'state', 'zipcode', 'phone', 'email']
                for field in required_fields:
                    if not request.form.get(field):
                        flash(f'The field "{field.replace("_", " ").title()}" is required.', 'error')
                        return redirect(url_for('checkout'))

                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                country = request.form.get('country')
                address = request.form.get('address')
                city = request.form.get('city')
                state = request.form.get('state')
                zipcode = request.form.get('zipcode')
                phone = request.form.get('phone')
                email = request.form.get('email')

                
                total_price = 0
                cart_items = Cart.query.filter_by(user_id=user_id).all()
                
                # this is very  important for creating an order if the place order is pressesd
                order = Order(
                    buyer_id=user_id,
                    date=datetime.utcnow(),
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    address=address,
                    city=city,
                    state=state,
                    zipcode=zipcode,
                    phone=phone,
                    email=email,
                    status=0  
                )
                db.session.add(order)

                #after the order is added, the cart must be cleared
                for cart_item in cart_items:
                    item_id = cart_item.item_id
                    Cart.query.filter_by(item_id=item_id).delete()
                    db.session.commit()

                    # also, as our brand mainly depend on the used or second hand items so there is only one item so it will be deleted if ordered
                    item = Item.query.get(item_id)
                    if item:
                        db.session.delete(item)
                        db.session.commit()

                flash('Your order has been placed successfully!')
                return render_template('OrderTracking.html', order=order)
    
    return render_template('checkout.html', items=items, total_price= total_price_with_tax)

    
#OrderTracking
@app.route('/OrderTracking')
def order_summary():
    return render_template('OrderTracking.html')

#Login
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        
        #this is for authentication if the user is registered or not
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Successful login, set user ID in session
            session['user_id'] = user.id
            return redirect(url_for('index'))  
        else:
            # Invalid credentials
            return render_template('Login.html', error='Invalid credentials')

    return render_template('Login.html')

# Logout
@app.route('/logout')
def logout():
    # to logout this means the userid is popped from the current sessions
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
    #to sell item then when add item button is clicked this will happen
    if request.method == 'POST':
        title = request.form.get('title')
        email = request.form.get('email')
        phone = request.form.get('phone')
        type = request.form.get('type')
        discription = request.form.get('description')
        location = request.form.get('location')
        status = request.form.get('itemStatus')
        priceType = int(request.form.get('priceType'))  

        #if the choosen type is free, then the price is set to 0
        if(priceType==0):
            price = 0
        else:
            price = request.form.get('priceInput')

        user_id = session.get('user_id')
        rate =int(request.form.get('rating')) + 1

        image = request.form.get(f'imageUpload0')

        #creating the new item in the database
        newItem = Item(name=title, description= discription, price=price, image= image, quantity=1, rate=rate, category_id=int(type), user_id=user_id )
 
        db.session.add(newItem)
        db.session.commit()

        # [show message ]
        flash('Your item has been added successfully!')
        print('Flash message set')
        return redirect(url_for('published'))

    return render_template('Sellitem.html')



#Search
@app.route('/basic',methods=['POST'])
def search():
    #this is to get the query from the search and strip it
    query = request.form.get('query', '').strip()
    #then start to match the query with the name or description
    if query:
        items = Item.query.filter(
            (Item.name.ilike(f'%{query}%')) |
            (Item.description.ilike(f'%{query}%'))
        ).all()
        
        #after that we got all the matched items to appear in the search result page
        if items:
            categories = [get_category_name(item.category_id) for item in items]
            return render_template('search_results.html', items=items, categories=categories, query=query)
        else:
            flash('No results found for "{}"'.format(query))
            return render_template('search_results.html')
        return redirect(request.referrer or url_for('index'))


#Subscribe
@app.route('/subscribtion',methods=['POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form.get('email1')

        # Check if the email is already subscribed
        existing_subscription = Subscription.query.filter_by(user_email=email).first()
        if existing_subscription:
            flash('You are already subscribed!')
        else:
         
            new_subscription = Subscription(user_email=email)

            # Add the new subscription to the database
            db.session.add(new_subscription)
            db.session.commit()

            flash('You have been successfully subscribed!')

        # Redirect to the appropriate page after subscription
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    