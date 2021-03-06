from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit= SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Enter Password Again', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Already registered')


class ResetPasswordRequestForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    submit= SubmitField('Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password Again', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class UploadForm(FlaskForm):
    photo = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg'], 'Please upload an Image')])
    submit = SubmitField('Upload')

class VirtualIDForm(FlaskForm):
    submit = SubmitField('Generate Virtual ID')

