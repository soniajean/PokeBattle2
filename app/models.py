from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


catch = db.Table(
    'catch',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
)

pokesquadTable = db.Table(
    'pokesquadTable',
    db.Column('name', db.String, db.ForeignKey('pokemon.name'), nullable=False),
    db.Column('id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    caught = db.relationship('Pokemon',
        #this is multi-join!
        # c is short for column
        secondary = 'catch',
        backref = 'caught',
        lazy = 'dynamic'
    )


    def catch(self, pokemon):
        self.caught.append(pokemon)
        db.session.commit()

    def released(self, pokemon):
        self.caught.remove(pokemon)
        db.session.commit()


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) 
        #self.password = password   ---OLD  not hashed

    def saveUser(self):
        db.session.add(self)
        db.session.commit()


       
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    ability = db.Column(db.String, nullable=False)
    base_xp = db.Column(db.Integer, nullable=False)
    front_shiny = db.Column(db.String, nullable=False, unique=True)
    base_atk = db.Column(db.Integer, nullable=False)
    base_hp = db.Column(db.Integer, nullable=False)
    base_def = db.Column(db.Integer, nullable=False)
    caught_flag = db.Column(db.Boolean) 
    def __init__(self, name, ability, base_xp, front_shiny, base_atk, base_hp, base_def):
        self.name = name
        self.ability = ability
        self.base_xp = base_xp
        self.front_shiny = front_shiny
        self.base_atk = base_atk
        self.base_hp = base_hp
        self.base_def = base_def

    def savePokemon(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

