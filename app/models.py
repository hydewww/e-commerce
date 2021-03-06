import datetime
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    items = db.relationship('Item', secondary='carts', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    def __repr__(self):
        return self.name

class AnonymousUser(AnonymousUserMixin):
    pass

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Cate(db.Model):
    __tablename__ = 'cates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    items = db.relationship('Item', backref='cate')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Integer)
    num = db.Column(db.Integer)
    desc = db.Column(db.Text)
    owner_id = db.Column(db.Integer)
    cate_id = db.Column(db.Integer, db.ForeignKey('cates.id'))
    img = db.Column(db.String(16), unique=True)
    orders = db.relationship('Order', secondary='order_item', backref='item')
    users = db.relationship('User', secondary='carts', backref='item')

    def __init__(self, name, price, num, desc, cate_id, owner_id):
        self.name = name
        self.price = price
        self.num = num
        self.desc = desc
        self.cate_id = cate_id
        self.owner_id = owner_id

    def __repr__(self):
        return '<Item %r>' % self.name


class Status:
    ORDERED = 0
    PAIED = 1
    DELIVERED = 2
    RECEIVED = 3
    

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    status = db.Column(db.Integer, default=Status.ORDERED)
    items = db.relationship('Item', secondary='order_item', backref='order')

    def __init__(self, buyer_id, owner_id):
        self.buyer_id = buyer_id
        self.owner_id = owner_id


class Order_Item(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    num = db.Column(db.Integer)

    def __init__(self, order_id, item_id, num):
        self.order_id = order_id
        self.item_id = item_id
        self.num = num


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    num = db.Column(db.Integer, default=1)

    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id
