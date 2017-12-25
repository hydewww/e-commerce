from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Item, Cate

class ItemForm(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    num = IntegerField('Num')
    desc = TextField('Description')
    cate = StringField('Category')
    submit = SubmitField('Upload')
