from flask import render_template, request, redirect, url_for
from . import buy
from .. import db,images,imag_name
from ..models import Item, Order, Cart, Order_Item
from flask_login import login_required, current_user
from sqlalchemy import desc

@buy.route("/cart")
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    items = current_user.items
    return render_template("buy/cart.html", items=items, cart=cart)


@buy.route("/order")
@login_required
def order():
    orders = Order.query.filter_by(buyer_id=current_user.id).all()
    itemslist = []
    for order in orders:
        items = Order_Item.query.filter_by(order_id=order.id).all()
        itemslist.append(items)
    return render_template("buy/order.html", orders=orders, itemslist=itemslist,images=images,imag_name=imag_name)


@buy.route("/add2cart/<int:id>")
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
    return redirect(url_for('buy.cart'))


@buy.route("/buy/cart")
@login_required
def buy_cart():
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    if carts is None:
        return redirect(url_for("main.index"))
    shop_order = {}
    for cart in carts:
        item = Item.query.filter_by(id=cart.item_id).first()
        owner_id = item.owner_id
        if owner_id not in shop_order.keys():
            order = Order(buyer_id=current_user.id, owner_id=owner_id)
            db.session.add(order)
            db.session.commit()
            order = Order.query.filter_by(buyer_id=current_user.id).order_by(desc(Order.date)).first()          
            shop_order[owner_id] = order.id
            order_item = Order_Item(order_id=order.id, item_id=cart.item_id, num=cart.num)
            item.num = item.num - cart.num
            db.session.add(item)
            db.session.add(order_item)
            db.session.delete(cart)
        else:
            order_id = shop_order[owner_id]
            order_item = Order_Item(order_id=order_id, item_id=cart.item_id, num=cart.num)
            item.num = item.num - cart.num
            db.session.add(item)
            db.session.add(order_item)
            db.session.delete(cart)
    db.session.commit()
    # order = Order(buyer_id=current_user.id)
    # db.session.add(order)
    # db.session.commit()
    # order = Order.query.filter_by(buyer_id=current_user.id).order_by(desc(Order.date)).first()
    # for cart_item in cart_items:
    #     order_item = Order_Item(order_id=order.id, item_id=cart_item.item_id, num=cart_item.num)
    #     db.session.add(order_item)
    #     db.session.delete(cart_item)
    # db.session.commit()
    return redirect(url_for("buy.order"))


@buy.route("/buy/<int:id>")
@login_required
def buy(id):
    item = Item.query.filter_by(id=id).first_or_404()
    order = Order(buyer_id=current_user.id, owner_id=item.owner_id)
    db.session.add(order)
    db.session.commit()
    order = Order.query.filter_by(buyer_id=current_user.id, owner_id=item.owner_id).order_by(desc(Order.date)).first()
    order_item = Order_Item(order_id=order.id, item_id=item.id, num=1)
    item.num = item.num - 1
    db.session.add(item)
    db.session.add(order_item)
    db.session.commit()
    return redirect(url_for("buy.order"))
