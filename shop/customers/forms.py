from wtforms import Form, DateTimeField, IntegerField, BooleanField, StringField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register



class CustomerForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Re-enter Password')
    phone = IntegerField('Phone Number', [validators.DataRequired()])
    institution = StringField('Institution', [validators.DataRequired()])
    major = StringField('Major', [validators.DataRequired()])
    semester = IntegerField('Semester', [validators.DataRequired()])
    birthday = DateTimeField('Birthday (dd/mm/yy)', format='%d/%m/%Y')

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("The Username is Taken")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This Email is Already Registered")

class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])

 