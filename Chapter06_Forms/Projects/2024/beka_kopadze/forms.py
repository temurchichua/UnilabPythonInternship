from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, length

class PersonalForm(FlaskForm):

    name = StringField("სახელი", validators=[DataRequired(), length(max=20)])
    surname = StringField("გვარი", validators=[DataRequired(), length(max=20)])
    image = FileField("სურათის ლინკი", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField("შენახვა")