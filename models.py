from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) ##
    phone_number = db.Column(db.String(20), nullable=False) ##
    address=db.Column(db.String(200), nullable=False)
    items = db.relationship('Item', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    cart=db.relationship('Cart',backref='user',uselist=False,lazy=True)

    def __init__(self, email, password, phone_number, username, address):
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.username = username
        self.address = address
        
    def __repr__(self):
        return '<User %r>' % self.username

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

    def __repr__(self):
        return '<Category %r>' % self.name

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=True)  # Path to image file
    quantity=db.Column(db.Integer,nullable=False,default=1)
    rate=db.Column(db.Integer,nullable=False)
    db.CheckConstraint("rate>0 AND rate <11")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #orders = db.relationship('Order', backref='item', lazy=True)
    reviews = db.relationship('Review', backref='item', lazy=True)
    cart=db.relationship('Cart',lazy=True)

    def __repr__(self):
        return '<Item %r>' % self.name


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Review %r>' % self.id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Message %r>' % self.id


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.name}>'


class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    total_payment=db.Column(db.Integer,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id=db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __repr__(self):
        return f'<Cart {self.id}>'

order_item = db.Table('order_item',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Integer, default=0)  # 0 for ordered, 1 for shipped, 2 for delivered
    
    items = db.relationship('Item', secondary='order_item', backref='orders', lazy=True)

    def __repr__(self):
        return '<Order %r>' % self.id

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email=db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Order %r>' % self.id

class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)

    def __init__(self, code, discount_percentage):
        self.code = code
        self.discount_percentage = discount_percentage

    def __repr__(self):
        return f'<PromoCode {self.code}>'

    @classmethod
    def create(cls, code, discount_percentage):
        promo_code = cls(code=code, discount_percentage=discount_percentage)
        db.session.add(promo_code)
        db.session.commit()
        return promo_code

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    def update(self, code, discount_percentage):
        self.code = code
        self.discount_percentage = discount_percentage
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()