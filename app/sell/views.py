from flask import render_template, redirect, url_for, flash
from . import sell
from .. import db, images
from ..models import Item, Cate, Order_Item, Order
from flask_login import login_required, current_user
from .forms import ItemForm


@sell.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = ItemForm()
    if form.validate_on_submit():
        cate = Cate.query.filter_by(name=form.cate.data).first()
        if not cate:
            cate = Cate(name=form.cate.data)
            db.session.add(cate)
            db.session.commit()
            cate = Cate.query.filter_by(name=form.cate.data).first()

        item = Item(name=form.name.data,
                    price=form.price.data,
                    num=form.num.data,
                    desc=form.desc.data,
                    cate_id=cate.id,
                    owner_id=current_user.id
                    )
        db.session.add(item)
        db.session.commit()
        filename = images.save(form.image.data, name=str(item.id)+'.')
        item.img = filename
        db.session.add(item)
        db.session.commit()
        flash("Upload Success.")
        return redirect(url_for('sell.upload'))
    return render_template("sell/upload.html", form=form)


@sell.route('/order')
@login_required
def order():
    # orders = Order.query.filter_by(owner_id=current_user.id).all()
    orders = db.session.execute("SELECT * FROM orders WHERE orders.owner_id="+str(current_user.id)).fetchall()
    itemslist = []
    img_dict = {}
    for order in orders:
        # items = Order_Item.query.filter_by(order_id=order.id).all()
        items = db.session.execute("SELECT * FROM order_item WHERE order_item.order_id="+str(order.id)).fetchall()
        for item in items:
            # item_img = Item.query.filter_by(id=item.item_id).first().img
            item_imgg = db.session.execute("SELECT * FROM items WHERE items.id=" + str(item.item_id)).fetchone()
            item_img = item_imgg.img
            img_dict[item.item_id] = item_img
        itemslist.append(items)
    return render_template("sell/order.html", orders=orders, itemslist=itemslist, images=images, img_dict=img_dict)


@sell.route('/deliver/<int:order_id>')
@login_required
def deliver(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    if order.owner_id == current_user.id and order.status == 1:
        order.status = 2
        db.session.add(order)
        db.session.commit()
        flash("Deliver Success")
    return redirect(url_for("sell.order"))
