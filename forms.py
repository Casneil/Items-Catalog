#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,\
 BooleanField
from wtforms.validators import DataRequired, Length, Email, \
 EqualTo, ValidationError

   # Making the Registration Form #
class RegistrationForm(FlaskForm):
   # Validating username #	
	username = StringField('username',\
		validators=[DataRequired(),\
		 Length(min=6, max=15)])
   # Validating email #	
	email = StringField('email',\
		validators=[DataRequired(),\
		Length(min=6, max=15)])
   # Validating password #	
	password = PasswordField('Password',\
		validators=[DataRequired(),\
		Length(min=6, max=30)])	
   # Confirming password #
	confirm_password = PasswordField('Confirm\
		 Password',validators=[DataRequired(),\
		 EqualTo('password'),\
		 Length(min=6, max=30)])	
   # Submiting password #
	submit = SubmitField('Sign-Up')	

	## To Do ##

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Username taken')
    
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('Email is taken.')


class LoginForm(FlaskForm):


	email = StringField('email',\
		validators=[DataRequired(),\
		Length(min=6, max=30)])

	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


	password = PasswordField('Password',\
		validators=[DataRequired(),\
		Length(min=6, max=30)])	


