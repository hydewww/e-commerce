from flask import render_template, request, redirect, url_for
from . import private
from .. import db
from ..models import Item, Order, Cart, Order_Item
from flask_login import login_required, current_user
from sqlalchemy import desc

@private.route("/cart")
@login_required
def cart():
    items = current_user.items
    return render_template("private/cart.html", items=items)


@private.route("/order")
@login_required
def order():
    orders = Order.query.filter_by(buyer_id=current_user.id).all()
    return render_template("private/order.html", orders=orders)


@private.route("/add2cart/<int:id>")
@login_required
def add2cart(id):
    item = Item.query.filter_by(id=id).first_or_404()
    cart = Cart.query.filter_by(user_id=current_user.id, item_id=item.id).first()
    if cart:
        cart.num += 1
    else:
        cart = Cart(user_id=current_user.id, item_id=item.id)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('main.index'))


@private.route("/buy/cart")
@login_required
def buy_cart():
    cart_items = Cart.query.filter(user_id=current_user.id).all()
    if cart_items is None:
        return redirect(url_for("main.index"))
    order = Order(buyer_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    order = Order.query.filter_by(buyer_id=current_user.id).order_by(desc(Order.date)).first()
    for cart_item in cart_items:
        order_item = Order_Item(order_id=order.id, item_id=cart_item.item_id, num=cart_item.num)
        db.session.add(order_item)
        db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for("private.order"))


@private.route("/buy/<int:id>")
@login_required
def buy(id):
    item = Item.query.filter_by(id=id).first_or_404()
    order = Order(buyer_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    order = Order.query.filter_by(buyer_id=current_user.id).order_by(desc(Order.date)).first()
    order_item = Order_Item(order_id=order.id, item_id=item.id, num=1)
    db.session.add(order_item)
    db.session.commit()
    return redirect(url_for("private.order"))
