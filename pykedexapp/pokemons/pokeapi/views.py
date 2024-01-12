import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache


def fetch_with_requests(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def update_progress(progress_key, increment=1):
    current_progress = cache.get(progress_key, 0)
    cache.set(progress_key, current_progress + increment, timeout=3600)


def get_pokemon_species_data(species_url):
    species_data = fetch_with_requests(species_url) or {}
    return next(
        (entry['flavor_text'] for entry in species_data.get('flavor_text_entries', []) if
         entry['language']['name'] == 'en'),
        ''
    )


def get_pokemon_detail(pokemon_url, progress_key=None):
    pokemon_data = fetch_with_requests(pokemon_url)
    if not pokemon_data:
        return None

    species_url = pokemon_data['species']['url']
    description = get_pokemon_species_data(species_url)
    special_ability = next(
        (ability['ability']['name'] for ability in pokemon_data['abilities'] if ability['is_hidden']),
        ''
    )

    pokemon = {
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
    if progress_key:
        update_progress(progress_key)
    return pokemon


def get_pokemon_data(request, query_type, query_value=None, limit=1, offset=0):
    cache_key = 'all_pokemon'
    all_pokemon_data = cache.get(cache_key)

    try:
        if all_pokemon_data:
            if query_type == 'name':
                pokemon_data = next((p for p in all_pokemon_data if p['name'] == query_value), None)
            elif query_type == 'id':
                pokemon_data = next((p for p in all_pokemon_data if str(p['id']) == query_value), None)
            elif query_type == 'search':
                pokemon_data = [p for p in all_pokemon_data if query_value in p['name']][offset:offset + limit]
            elif query_type == 'some':
                pokemon_data = all_pokemon_data[offset:offset + limit]
            elif query_type == 'all':
                pokemon_data = all_pokemon_data
            else:
                return Response({'message': 'Invalid query type'}, status=400)

            if len(pokemon_data) == 0:
                return Response({'message': 'Pokemon not found'}, status=404)
            return Response(pokemon_data)
        else:
            if query_type in ['name', 'id']:
                pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{query_value}'
                pokemon = get_pokemon_detail(pokeapi_url)
                if pokemon:
                    return Response(pokemon)
                else:
                    return Response({'message': 'Pokemon not found or error in PokeAPI'}, status=404)


            elif query_type == 'search':
                pokeapi_url = f'https://pokeapi.co/api/v2/pokemon?limit=1118&offset=0'
                response = requests.get(pokeapi_url)
                if response.status_code == 200:
                    all_pokemon_data = response.json()['results']
                    detailed_pokemon_data = []
                    for p in all_pokemon_data:
                        if query_value in p['name']:
                            detailed_pokemon = get_pokemon_detail(p['url'])
                            if detailed_pokemon:
                                detailed_pokemon_data.append(detailed_pokemon)
                    pokemon_data = detailed_pokemon_data[offset:offset + limit]
                    if not pokemon_data:
                        return Response([], status=404)
                    return Response(pokemon_data)
                else:
                    return Response({'message': 'Pokemon not found or error in PokeAPI'}, status=404)


            elif query_type == 'some':
                pokeapi_url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}'
                response = requests.get(pokeapi_url)
                if response.status_code == 200:
                    all_pokemon_data = response.json()['results']
                    detailed_pokemon_data = []
                    for p in all_pokemon_data:
                        detailed_pokemon = get_pokemon_detail(p['url'])
                        if detailed_pokemon:
                            detailed_pokemon_data.append(detailed_pokemon)
                    return Response(detailed_pokemon_data)
                else:
                    return Response({'message': 'Pokemon not found or error in PokeAPI'}, status=404)

            elif query_type == 'all':
                pokeapi_url = f'https://pokeapi.co/api/v2/pokemon?limit=1118&offset=0'
                response = requests.get(pokeapi_url)
                if response.status_code == 200:
                    all_pokemon_data = response.json()['results']
                    detailed_pokemon_data = []
                    for p in all_pokemon_data:
                        detailed_pokemon = get_pokemon_detail(p['url'])
                        if detailed_pokemon:
                            detailed_pokemon_data.append(detailed_pokemon)
                    return Response(detailed_pokemon_data)
                else:
                    return Response({'message': 'Pokemon not found or error in PokeAPI'}, status=404)


            else:
                return Response({'message': 'Invalid query type'}, status=400)
    except Exception as e:
        print(e)
        return Response({'message': 'Invalid query type'}, status=400)


@api_view(['GET'])
def get_pokemon_from_pokeapi_by_name(request, name):
    return get_pokemon_data(request, 'name', name)


@api_view(['GET'])
def get_pokemon_from_pokeapi_by_id(request, id):
    return get_pokemon_data(request, 'id', str(id))


@api_view(['GET'])
def get_some_pokemon_from_pokeapi(request, limit, offset):
    return get_pokemon_data(request, 'some', limit=limit, offset=offset)


@api_view(['GET'])
def get_pokemon_from_pokeapi_by_search_term(request, search_letters, limit, offset):
    return get_pokemon_data(request, 'search', search_letters, limit, offset)


@api_view(['GET'])
def get_all_pokemon_from_pokeapi(request):
    return get_pokemon_data(request, 'all')


@api_view(['GET'])
def get_pokemon_fetch_progress(request, key):
    progress_key = f'progress_{key}'
    progress = cache.get(progress_key, 0)
    return Response({'progress': progress})
