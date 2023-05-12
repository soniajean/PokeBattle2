
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignUpForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    id = StringField('id', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField("Confirm", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    id = StringField('id', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField("Confirm", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class PokemonForm(FlaskForm):
    pokemon = StringField('Pokemon', validators = [DataRequired()])
    submit = SubmitField()

class ProfileForm(FlaskForm):
    id = StringField('id', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField("Confirm", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class Poke_Name(FlaskForm):
    poke_name = StringField('Search for Pokemon')
    submit = SubmitField()
   
