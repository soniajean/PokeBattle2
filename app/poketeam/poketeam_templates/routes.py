from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.models import Pokemon, User, pokesquadTable
from sqlalchemy import select
pokesquad = Blueprint('pokesquad', __name__, template_folder='pokesquad_templates')

@pokesquad.route('/catch/<string:pokename>')
def catchPokemon(pokename):
    pokemon = Pokemon.query.filter_by(name=pokename).first()
    if pokemon:
        current_user.catchPokemon(pokemon)
    return redirect(url_for('pokemonPage'))

@pokesquad.route('/release/<string:pokename>')
def releasePokemon(pokename):
    pokemon = Pokemon.query.get(pokename)
    if pokemon:
        current_user.releasePokemon(pokemon)

    return redirect(url_for('pokesquad.viewCurrentSquad'))

@pokesquad.route('/squad')
def viewSquad():
    users = current_user.squad.all()
    print(users)
    # d={}
    # d= [current_user.username] = users

    return render_template('pokesquad.html',users=users) 
    
   


@pokesquad.route('/current_squad')
def viewCurrentSquad():
    users = User.query.all()
    d = {}
    for u in users:
        d[u.username] = u.catchPokemon.all()
    return render_template((template_name_or_list))
    
@pokesquad.route('/battle')
def battleRoyale(user):
    user1 = User.query.filter(User == user).first()
    user2 = User.query.filter(User == current_user).first()
    print(user1.wins)

    pokesquad1 = user1.pokesquad.all()
    pokesquad2 = user2.pokesquad.all()

    health_defense_points1 = 0
    attack_points1 = 0
    health_defense_points2 = 0
    attack_points2 = 0

    for pokemon in pokesquad1:
        health_defense_points1 += pokemon.defense
        health_defense_points1 += pokemon.hp
        attack_points1 += pokemon.attack

    for pokemon in pokesquad2:
        health_defense_points2 += pokemon.defense
        health_defense_points2 += pokemon.hp
        attack_points2 += pokemon.attack

    overall_points_pokesquad1 = health_defense_points1 - attack_points2
    overall_points_pokesquad2 = health_defense_points2 - attack_points1

    if overall_points_pokesquad1 > overall_points_pokesquad2:
        user1.wins += 1
        user2.losses += 1
        user1.savePokemon()
        user2.savePokemon()


    elif overall_points_pokesquad1 < overall_points_pokesquad2:
        user1.losses += 1
        user2.wins += 1
        user1.savePokemon()
        user2.savePokemon()

        

    elif overall_points_pokesquad1 == overall_points_pokesquad2:
        user1.ties += 1
        user2.ties += 1
        user1.savePokemon()
        user2.savePokemon()


    return render_template('battleroyale.html', pokesquad1=pokesquad1, pokesquad2=pokesquad2, user1=user1, user2=user2, overall_points_pokesquad1=overall_points_pokesquad1, overall_points_pokesquad2=overall_points_pokesquad2)