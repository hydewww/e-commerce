from flask import render_template, request, redirect, url_for, flash
from . import buy
from .. import db, images
from ..models import Item, Order, Cart, Order_Item
from flask_login import login_required, current_user
from sqlalchemy import desc


@buy.route("/cart")
@login_required
def cart():
    # cart = Cart.query.filter_by(user_id=current_user.id).all()
    cart = db.session.execute("SELECT * FROM carts WHERE carts.user_id="+str(current_user.id)).fetchall()
    items = current_user.items
    return render_template("buy/cart.html", items=items, cart=cart, images=images)


@buy.route("/order")
@login_required
def order():
    # orders = Order.query.filter_by(buyer_id=current_user.id).all()
    orders = db.session.execute("SELECT * FROM orders WHERE orders.buyer_id="+str(current_user.id)).fetchall()
    itemslist = []
    img_dict = {}
    for order in orders:
        # items = Order_Item.query.filter_by(order_id=order.id).all()
        items = db.session.execute("SELECT * FROM order_item WHERE order_item.order_id="+str(order.id)).fetchall()
        for item in items:
            # item_img = Item.query.filter_by(id=item.item_id).first().img
            item_imgg = db.session.execute("SELECT * FROM items WHERE items.id="+str(item.item_id)).fetchone()
            item_img = item_imgg.img
            img_dict[item.item_id] = item_img
        itemslist.append(items)
    return render_template("buy/order.html", orders=orders, itemslist=itemslist, images=images, img_dict=img_dict)


@buy.route("/add2cart/<int:id>")
@login_required
def add2cart(id):
    # item = Item.query.filter_by(id=id).first_or_404()
    item = db.session.execute("SELECT * FROM items WHERE items.id="+str(id)).fetchone()
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
    return redirect(url_for("buy.order"))


@buy.route("/buy_item/<int:id>")
@login_required
def buy_item(id):
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


@buy.route("/pay/<int:order_id>")
@login_required
def pay(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    if order.buyer_id == current_user.id and order.status == 0:
        order.status = 1
        db.session.add(order)
        db.session.commit()
        flash("Pay Success")
    return redirect(url_for("buy.order"))


@buy.route("/receive/<int:order_id>")
@login_required
def receive(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    if order.buyer_id == current_user.id and order.status == 2:
        order.status = 3
        db.session.add(order)
        db.session.commit()
        flash("Receive Success")
    return redirect(url_for("buy.order"))
