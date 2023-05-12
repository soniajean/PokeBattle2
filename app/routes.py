
from app import app

from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required

from .auth.forms import SignUpForm, LoginForm, ProfileForm
from .models import User, Pokemon
from .auth.forms import PokemonForm
from .services import getPokemon
import requests, json

# app = Blueprint('catch', __name__, template_folder='ig_templates')

@pokesquad.route('/squad')
def viewSquad():
    users = current_user.squad.all()
    print(users)
    # d={}
    # d= [current_user.username] = users
    return render_template('pokesquad.html',users=users)

@app.route('/')
def homePage():
    users = User.query.all()
    # users = User.query.limit(20)
    catch_set = set()

    if current_user.is_authenticated:
        users_caught = current_user.caught.all()
        print(users_caught)
        for u in users_caught:
            catch_set.add(u.id)
        for u in users:
            if u.id in catch_set:
                u.flag = True

    

    return render_template('index.html', users=users)


@app.route('/login')
def loginPage():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
        # SELECT * FROM user WHERE username = <username variable>
            if user:
                if check_password_hash(user.password, password):  # <--NEW
                #user.password == password:  --OLD way
                    flash('YAY, you\'re logged in!', 'success')
                    login_user(current_user)
                    
                    return redirect(url_for('homePage'))
                    
                else:
                    flash('WRONG password. . .', 'warning')
            else:
                flash('This isn\'t a user!', 'danger')
            return redirect(url_for('auth.loginPage'))
    return render_template('login.html', form=form)
   


@app.route('/signUp', methods=["GET", "POST"])
def signUpPage():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(username, email, password)


            user = User(username, email, password)            
            user.saveUser()
            return redirect(url_for('loginPage'))

    return render_template('signUp.html', form=form)

@app.route('/editProfile', methods=["GET", "POST"])
def ProfilePage():

    form = ProfileForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(username, email, password)


            user = User(username, email, password)            
            user.saveUser()
            return redirect(url_for('loginPage'))

    return render_template('ProfilePage.html', form=form)



@app.route('/pokemon_search', methods=["GET", "POST"])
def findpokemon():

    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():  
            pokemon = form.pokemon.data
            pokedict = Pokemon.query.filter_by(name=pokemon).first()
            full = False
            if current_user.caught.count() > 4:
                full = True
            c = current_user.caught.all()
            if pokedict in c:
                r = True
                if pokedict:
                    print(f'From Query')
                    return render_template('pokemon_search.html', form=form, r=r, full=full, pokedict=pokedict)
            

            getpoke= getPokemon(pokemon)
            name = getpoke['name']
            ability = getpoke['ability']
            base_xp = getpoke['base_xp']
            front_shiny = getpoke['front_shiny']
            base_atk = getpoke['base_atk']
            base_hp = getpoke['base_hp' ]
            base_def = getpoke['base_def']

            pokedict = Pokemon(name, ability, base_xp, front_shiny, base_atk, base_hp, base_def) 
            print(f'From API call')
            pokedict.savePokemon()            
            return render_template('pokemon_search.html', form=form, r=r, full=full, pokedict=pokedict)

    return render_template('pokemon_search.html', form=form)

@app.route('/catch/<int:pokemon_id>')
@login_required
def catch(pokemon_id):
    #to do we need to make the caught flag true

    p = Pokemon.query.get(pokemon_id)
    if not p:
        return redirect(url_for('homePage'))
    current_user.catch(p)
    return redirect(url_for('homePage'))

    # return render_template('pokemon_search.html', users_catched=users_catched)

@app.route('/releasepokemon/<int:pokemon_id>')
@login_required
def releasepokemon(pokemon_id):
    p = Pokemon.query.get(pokemon_id)
    if not p:
        return redirect(url_for('homePage'))
    current_user.catch(p)
    return redirect(url_for('homePage'))


    return render_template('pokemon_search.html', form=form, users_catched=users_catched)

   
