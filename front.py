import imp
from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import NumberRange

class DateForm(FlaskForm):
    date = StringField('date', validators=[NumberRange(min=0, max=2022)])
    submit = SubmitField('Post')
