from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class Register(FlaskForm):
    def validate_password(self, password):
        if len(password.data) < 10:
            raise ValidationError('Password should be at least 10 characters long') 

    username = StringField(label = 'Username', validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField(label = 'Email', validators=[DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label = 'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Sign Up')

class Login(FlaskForm):
    email = StringField(label = 'Email')
    password  = PasswordField(label = 'Password')
    submit = SubmitField(label = 'Log In')
    remember_me = BooleanField('Remember Me')
