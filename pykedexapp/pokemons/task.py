from django.core.cache import cache
import requests
from tqdm import tqdm

def get_pokemon_object(pokemon_data):
    special_ability = next(
        (ability['ability']['name'] for ability in pokemon_data['abilities'] if ability['is_hidden']),
        ''
    )
    description = next(
        (entry['flavor_text'] for entry in pokemon_data.get('flavor_text_entries', []) if entry['language']['name'] == 'en'),
        ''
    )

    return {
        'order': pokemon_data.get('order', 0),
        'name': pokemon_data.get('name', ''),
        'lvl': 1,
        'xp': pokemon_data.get('base_experience', 0),
        'number': pokemon_data.get('id', 0),
        'type_1': pokemon_data['types'][0]['type']['name'] if pokemon_data['types'] else '',
        'type_2': pokemon_data['types'][1]['type']['name'] if len(pokemon_data['types']) > 1 else '',
        'special_capacity': special_ability,
        'memo': description,
        'atck': pokemon_data['stats'][1]['base_stat'] if len(pokemon_data['stats']) > 1 else 0,
        'defs': pokemon_data['stats'][2]['base_stat'] if len(pokemon_data['stats']) > 2 else 0,
        'atck_spe': pokemon_data['stats'][3]['base_stat'] if len(pokemon_data['stats']) > 3 else 0,
        'defs_spe': pokemon_data['stats'][4]['base_stat'] if len(pokemon_data['stats']) > 4 else 0,
        'speed': pokemon_data['stats'][5]['base_stat'] if len(pokemon_data['stats']) > 5 else 0,
        'hp': pokemon_data['stats'][0]['base_stat'] if pokemon_data['stats'] else 0,
        'image_url': pokemon_data['sprites']['front_default'],
        'shiny_image_url': pokemon_data['sprites']['front_shiny']
    }

def cache_all_pokemon_data():
    if input('Voulez-vous mettre en cache les données des pokemons? (Prend plusieurs minutes mais recherches instantanées) [y/n] ') == 'y':
        pokeapi_url = 'https://pokeapi.co/api/v2/pokemon?limit=10&offset=0'
        response = requests.get(pokeapi_url)
        if response.status_code == 200:
            print('Caching all pokemon data...')
            all_pokemon_data = response.json()['results']

            for pokemon in tqdm(all_pokemon_data, desc='Caching Pokemons', unit='pokemon'):
                pokemon_url = pokemon['url']
                try:
                    response = requests.get(pokemon_url)
                    if response.status_code == 200:
                        pokemon_data = response.json()
                        pokemon_object = get_pokemon_object(pokemon_data)
                        pokemon.update(pokemon_object)
                except requests.RequestException as e:
                    print(f'Erreur lors de la récupération des données pour {pokemon_url}: {e}')

            cache.set('all_pokemon', all_pokemon_data, timeout=None)
            print('Mise en cache terminée.')
    else:
        print('Annulation de la mise en cache des données des pokemons.')


