from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from ..import images
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Item, Cate

class ItemForm(FlaskForm):
    image=FileField('image', validators=[FileAllowed(images,'only images'), FileRequired('please choose an image')])
    name = StringField('Name')
    price = IntegerField('Price')
    num = IntegerField('Num')
    desc = TextField('Description')
    cate = StringField('Category')
    submit = SubmitField('Upload')
