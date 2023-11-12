from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from notesfromkatieland.models import User, AllowedUser

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        userExists = User.query.filter_by(username=username.data).first()
        if userExists:
            raise ValidationError('Username already exists.')
    
    def validate_email(self, email):
        emailExists = User.query.filter_by(email=str.lower(email.data)).first()
        if emailExists:
            raise ValidationError('Email is taken.')
        
        emailAllowed = AllowedUser.query.filter_by(email=str.lower(email.data)).first()
        if emailAllowed is None:
            raise ValidationError('Email is not on the list of allowed users.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            userExists = User.query.filter_by(username=username.data).first()
            if userExists:
                raise ValidationError('Username already exists.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            emailExists = User.query.filter_by(email=email.data).first()
            if emailExists:
                raise ValidationError('Email is taken.')
            
            emailAllowed = AllowedUser.query.filter_by(email=email.data).first()
            if emailAllowed is None:
                raise ValidationError('Email is not on the list of allowed users.')
            
class ResendConfirmationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        emailExists = User.query.filter_by(email=email.data).first()
        if emailExists is None:
            raise ValidationError('There is no account with that email.')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        emailExists = User.query.filter_by(email=email.data).first()
        if emailExists is None:
            raise ValidationError('There is no account with that email.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')