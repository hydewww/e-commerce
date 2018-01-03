from flask import render_template, request, redirect, url_for
from . import public
from .. import db, images
from ..models import Item, Cate, User
from .forms import SearchForm


@public.route('/')
def index():
    #cates = Cate.query.all()
    cates = db.session.execute("SELECT * FROM cates").fetchall()
    # print(Cate.query)
    #items = Item.query.all()
    items = db.session.execute("SELECT * FROM items").fetchall()
    form = SearchForm()
    if form.validate_on_submit():
        items = Item.query.filter_by(name=form.itemname.data).all()
        return render_template("public/itemlist.html", items=items, cates=cates, images=images)
    return render_template("public/itemlist.html", items=items, cates=cates, images=images)


@public.route('/cate/<int:cate_id>')
def cate(cate_id):
    #cates = Cate.query.all()
    cates = db.session.execute("SELECT * FROM cates").fetchall()
    # items = Item.query.filter_by(cate_id=cate_id).all()
    # items = db.session.execute("""SELECT items.id AS items_id, items.name AS items_name, items.price AS items_price, items.num AS items_num, items."desc" AS items_desc, items.owner_id AS items_owner_id, items.cate_id AS items_cate_id, items.img AS items_img FROM items WHERE items.cate_id = """+str(cate_id)).fetchall()
    items = db.session.execute("SELECT  * FROM items WHERE items.cate_id = "+str(cate_id)).fetchall()
    #print(items)
    #print(Item.query.filter_by(cate_id=cate_id))
    form = SearchForm()
    if form.validate_on_submit():
        items = Item.query.filter_by(name=form.itemname.data).all()
        return render_template("public/itemlist.html", items=items, cates=cates, images=images)
    return render_template("public/itemlist.html", items=items, cates=cates, images=images)


@public.route('/owner/<int:owner_id>')
def owner(owner_id):
    #items = Item.query.filter_by(owner_id=owner_id).all()
    items = db.session.execute("SELECT * FROM items WHERE items.owner_id = "+str(owner_id)).fetchall()
    return render_template("public/itemlist.html", items=items, images=images)


@public.route('/item/<int:item_id>')
def item(item_id):
    item = db.session.execute("SELECT * FROM items WHERE items.id ="+str(item_id)).fetchone()
    owner = db.session.execute("SELECT * FROM users WHERE users.id ="+str(item.owner_id)).fetchone()
    cate = db.session.execute("SELECT * FROM cates WHERE cates.id="+str(item.cate_id)).fetchone()
    return render_template("public/item.html", item=item, images=images, owner=owner, cate=cate)
