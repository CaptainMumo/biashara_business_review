from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import User
#from flask_main import users

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    location = StringField("Location", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8,message="Password must be at least 8 characters long")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError("Ooopps! Username has already been taken!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError("Ooopps! An account with that email already exists!")

class SigninForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")

