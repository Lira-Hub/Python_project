from flask import Flask, render_template, flash, request,redirect
from wtforms import FlaskForm, TextField, TextAreaField, validators, StringField, SubmitField,PasswordField, ContactForm, BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidatonError, Email, Length, EqualTo)
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
#configuration of database I don't know if it is correct
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#app Configuration
DEBUG = True
app.config.from_object(__name__)
#this part of secret key I don't know how to get it
app.config['SECRET KEY'] = '1234567'

#building a class which will get the information from html form
class FormRegister(FlaskForm):
    username   = TextField('Name: ', validators=[validators.DataRequired()])
    email      = TextField('Email: ', validators=[validators.DataRequired(),validators.Length(min=6,max=35)])
    password   = PasswordField('New Password: ', validators=[validators.DataRequired(),validators.EqualTo('confirm', message='Password must match') validators.Lenght(min=6,max=35)])
    confirm    = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2018)', [validators.Required()])


#this is the route for registration
@app.route('/register', methods=['GET', 'POST'])
#this function will get the information from the class Register and add user to the Users database at the end
def register_users():
    form = FormRegister(request.form)

    if request.method=='POST' and form.validate():
        user = Users(form.username.data, form.email.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

#sort of database for te Users
class Users(db.Model):
    __tablename__ = "register_users"
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable = False)
    email    = db.Column(db.String, nullable = False)
    password = db.Column(db.Integer, nullable = False)

if __name__ == '__main__':
    with app.app_context():
        main()
