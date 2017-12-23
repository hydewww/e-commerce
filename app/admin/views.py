from flask import render_template, redirect, url_for, flash
from . import admin
from .. import db
from ..models import Item, Cate
from .forms import ItemForm

@admin.route('/upload', methods=['GET', 'POST'])
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
                    cate_id=cate.id
                    )
        db.session.add(item)
        db.session.commit()
        flash("Upload Success.")
        return redirect(url_for('admin.upload'))
    return render_template("admin/upload.html", form=form)
