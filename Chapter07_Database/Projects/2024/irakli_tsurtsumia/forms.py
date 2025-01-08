from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, length


class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), length(min=3, max=50)])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])

    submit = SubmitField('Submit')
