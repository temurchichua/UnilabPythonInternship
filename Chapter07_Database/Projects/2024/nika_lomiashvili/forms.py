from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired , FileAllowed, FileSize
from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, length, equal_to, ValidationError
from string import ascii_lowercase, ascii_uppercase, digits , punctuation

class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), length(min=6, max=64)])
    price = IntegerField("Price", validators=[DataRequired()])
    description = StringField("Description")
    img = FileField("Image", validators=[FileAllowed(["jpg", "png", "jpeg"], message="File type is not allowed")])

    submit = SubmitField("Save")


class RegisterField(FlaskForm):
    username = StringField("Fill Name", validators=[DataRequired()])
    password = PasswordField("Fill Password", validators=[length(min=8,max=64)])
    repeat_password = PasswordField("Repeat Password", validators=[equal_to("password")])
    gender = RadioField("Please indicate gender", choices=["Male", "Female"])
    country = SelectField("Select a country", choices=[
        ("georgia", "საქართველო"),
        ("germany", "გერმანია"),
        ("usa", "ამერიკა")
    ])
    birthday = DateField()
    about_you = TextAreaField()

    submit = SubmitField("Register")

    def validate_password(self, field):
        contains_uppercase = False
        contains_lowercase = False
        contains_digits = False
        contains_symbols = False
        for character in field.data:
            if character in ascii_uppercase:
                contains_uppercase = True
            if character in ascii_lowercase:
                contains_lowercase = True
            if character in punctuation:
                contains_symbols= True
        if not contains_uppercase:
            raise ValidationError("Password must contains Uppercase")
        if not contains_lowercase:
            raise ValidationError("Password must contains Lowercase")
        if not contains_digits:
            raise ValidationError("Password must contains Digits")
        if not contains_symbols:
            raise ValidationError("Password must contains Symbols")
        print(field.data)