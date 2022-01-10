from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from include.models import  User


class Register(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField(label = 'Email', validators=[DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label = 'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Sign Up')

    def validate_password(self, password):
        if len(password.data) < 10:
            raise ValidationError('Password should be at least 10 characters long') 
    
    def validate_email(self, attempted_email):
        email = User.query.filter_by(email = attempted_email.data).first()
        if email:
            raise ValidationError('Email already in use by another account!')

    def validate_username(self, attempted_username):
        username = User.query.filter_by(username = attempted_username.data).first()
        if username:
            raise ValidationError('Username taken')


class Login(FlaskForm):
    email = StringField(label = 'Email')
    password  = PasswordField(label = 'Password')
    submit = SubmitField(label = 'Log In')
    remember_me = BooleanField('Remember Me')


class UpdateAccount(FlaskForm):
    username = StringField(label = 'Username', validators=[DataRequired(), Length(min=5, max=40)])
    email = StringField(label = 'Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit1 = SubmitField(label = 'Update')
    
    def validate_email(self, attempted_email):
        if current_user.email != attempted_email.data:
            email = User.query.filter_by(email = attempted_email.data).first()
            if email:
                raise ValidationError('Email already in use by another account!')

    def validate_username(self, attempted_username):
        if current_user.username != attempted_username.data:
            username = User.query.filter_by(username = attempted_username.data).first()
            if username:
                raise ValidationError('Username taken')


class UpdatePassword(FlaskForm):
    current_password  = PasswordField(label = 'Current Password')
    new_password = PasswordField(label = 'New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label = 'Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit2 = SubmitField(label = 'Update')

    def validate_current_password(self, attempted_password):
        if not current_user.check_password(attempted_password.data):
            raise ValidationError('Incorrect Password!')

    def validate_new_password(self, password):
        if len(password.data) < 10:
            raise ValidationError('Password should be at least 10 characters long') 


class RequestResetForm(FlaskForm):
    email = StringField(label = 'Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label = 'Request Reset')

    def validate_username(self, email):
        username = User.query.filter_by(email = email.data).first()
        if username is None:
            raise ValidationError('User with this email does not exists!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(label = 'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Reset Password')

    def validate_new_password(self, password):
        if len(password.data) < 10:
            raise ValidationError('Password should be at least 10 characters long') 