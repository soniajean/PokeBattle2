import requests

def getPokemon(pokemon):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    if response.ok:
        my_dict = response.json()
        pokemon_dict = {}
        pokemon_dict["name"] = my_dict["name"]
        pokemon_dict["ability"] = my_dict["abilities"][0]["ability"]["name"]
        pokemon_dict["base_xp"] = my_dict["base_experience"]
        pokemon_dict["front_shiny"] = my_dict["sprites"]["front_shiny"]
        pokemon_dict["base_atk"] = my_dict["stats"][1]["base_stat"]
        pokemon_dict["base_hp"] = my_dict["stats"][0]["base_stat"]
        pokemon_dict["base_def"] = my_dict["stats"][2]["base_stat"]

        
        return pokemon_dict