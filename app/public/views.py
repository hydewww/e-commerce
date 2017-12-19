from flask import render_template, request, redirect, url_for
from . import public
from .. import db
from ..models import Item


@public.route('/')
def index():
    items = Item.query.all()
    return render_template("public/itemlist.html", items=items)


@public.route('/cate/<int:cate_id>')
def cate(cate_id):
    items = Item.query.filter_by(cate_id=cate_id).all()
    return render_template("public/itemlist.html", items=items)


@public.route('/item/<int:item_id>')
def item(item_id):
    item = Item.query.filter_by(id=item_id).first_or_404()
    return render_template("public/item.html", item=item)
