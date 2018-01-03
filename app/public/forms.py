from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from wtforms import ValidationError
from ..models import Item


class SearchForm(FlaskForm):
    itemname = StringField('Item Name', validators=[
                                        Required(), Length(1, 64)])
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if not Item.query.filter_by(itemname=field.data).first():
            raise ValidationError('No Such Item.')
