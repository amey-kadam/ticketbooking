from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

# User Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Custom validation to check if the username is already in use
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    # Custom validation to check if the email is already in use
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

# User Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Admin Form for Adding Museums
class AddMuseumForm(FlaskForm):
    name = StringField('Museum Name', 
                       validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', 
                        validators=[DataRequired(), Length(min=2, max=100)])
    district = StringField('District', 
                           validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City', 
                       validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Museum')

# Ticket Booking Form (Chatbot-based)
class BookTicketForm(FlaskForm):
    # Dropdowns or SelectFields for locations based on user input
    state = SelectField('State', choices=[], validators=[DataRequired()])
    city = SelectField('City', choices=[], validators=[DataRequired()])
    submit = SubmitField('Book Ticket')

# View Previous Tickets Form (if required)
class ViewTicketsForm(FlaskForm):
    submit = SubmitField('View My Tickets')
