#     # The following are the endpoints for the PokeAPI
#     # https://pokeapi.co/docs/v2/pokemon
#     ('pokeapi/get/one/<str:name>', views.get_pokemon_from_pokeapi_by_name),
#     ('pokeapi/get/one/<int:id>', views.get_pokemon_from_pokeapi_by_id),
#     ('pokeapi/get/some/<int:limit>/<int:offset>', views.get_some_pokemon_from_pokeapi),
#     ('pokeapi/get/some/<str:name>', views.get_some_pokemon_from_pokeapi_by_letters),
#     ('pokeapi/get/all', views.get_all_pokemon_from_pokeapi),
#
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from pykedexapp.pokemons.models import Pokemon


@api_view(['GET'])
def get_pokemon_from_pokeapi_by_name(request, name):
    """
    Get a pokemon from the PokeAPI by name.
    :param request: the Django HttpRequest object.
    :param name: the name of the pokemon.
    :return: JsonResponse with pokemon data or an error response.
    """
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{name}'

    try:
        response = requests.get(pokeapi_url)

        # Check if the response from PokeAPI is successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            # If the Pokémon is not found or any other error occurs
            return HttpResponseNotFound({'message': 'Pokemon not found or error in PokeAPI'})

    except requests.RequestException as e:
        # Log the exception (you can use Django's logging mechanism)
        # log.exception("Error fetching data from PokeAPI: %s", e)
        return HttpResponseBadRequest({'message': 'Error in fetching data from PokeAPI'})


@api_view(['GET'])
def get_pokemon_from_pokeapi_by_id(request, id):
    """
    Get a pokemon from the PokeAPI by id.
    :param request: the Django HttpRequest object.
    :param id: the id of the pokemon.
    :return: JsonResponse with pokemon data or an error response.
    """
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon/{id}'

    try:
        response = requests.get(pokeapi_url)

        # Check if the response from PokeAPI is successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            # If the Pokémon is not found or any other error occurs
            return HttpResponseNotFound({'message': 'Pokemon not found or error in PokeAPI'})

    except requests.RequestException as e:
        # Log the exception (you can use Django's logging mechanism)
        # log.exception("Error fetching data from PokeAPI: %s", e)
        return HttpResponseBadRequest({'message': 'Error in fetching data from PokeAPI'})


@api_view(['GET'])
def get_some_pokemon_from_pokeapi(request, limit, offset):
    """
    Get some pokemon from the PokeAPI by limit and offset.
    :param request: the Django HttpRequest object.
    :param limit: the limit of the pokemon.
    :param offset: the offset of the pokemon.
    :return: JsonResponse with pokemon data or an error response.
    """
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}'

    try:
        response = requests.get(pokeapi_url)

        # Check if the response from PokeAPI is successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            # If the Pokémon is not found or any other error occurs
            return HttpResponseNotFound({'message': 'Pokemon not found or error in PokeAPI'})

    except requests.RequestException as e:
        # Log the exception (you can use Django's logging mechanism)
        # log.exception("Error fetching data from PokeAPI: %s", e)
        return HttpResponseBadRequest({'message': 'Error in fetching data from PokeAPI'})


@api_view(['GET'])
def get_all_pokemon_from_pokeapi(request):
    """
    Get all pokemon from the PokeAPI.
    :param request: the Django HttpRequest object.
    :return: JsonResponse with pokemon data or an error response.
    """
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon'

    try:
        response = requests.get(pokeapi_url)

        # Check if the response from PokeAPI is successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            # If the Pokémon is not found or any other error occurs
            return HttpResponseNotFound({'message': 'Pokemon not found or error in PokeAPI'})

    except requests.RequestException as e:
        # Log the exception (you can use Django's logging mechanism)
        # log.exception("Error fetching data from PokeAPI: %s", e)
        return HttpResponseBadRequest({'message': 'Error in fetching data from PokeAPI'})


@api_view(['GET'])
def get_some_pokemon_from_pokeapi_by_letters(request, name):
    # first get all pokemon from pokeapi
    pokeapi_url = f'https://pokeapi.co/api/v2/pokemon?limit=1118&offset=0'
    try:
        response = requests.get(pokeapi_url)
        # Check if the response from PokeAPI is successful
        if response.status_code == 200:
            # get all pokemon names
            pokemon_names = []
            for pokemon in response.json()['results']:
                pokemon_names.append(pokemon['name'])
            # filter pokemon names by letters
            # if name is 'bul' then filtered_pokemon_names = ['bulbasaur', 'bulbasaur-1', 'bulbasaur-2']
            filtered_pokemon_names = list(filter(lambda x: name in x, pokemon_names))
            # return all pokemon object that match the filtered_pokemon_names
            # if name is 'bul' then pokemon_objects = [bulbasaur_object, bulbasaur-1_object, bulbasaur-2_object]
            pokemon_objects = []
            for pokemon_name in filtered_pokemon_names:
                pokemon_objects.append(Pokemon.objects.get(name=pokemon_name))
            # return pokemon_objects
            return Response(pokemon_objects)
    except requests.RequestException as e:
        # Log the exception (you can use Django's logging mechanism)
        # log.exception("Error fetching data from PokeAPI: %s", e)
        return HttpResponseBadRequest({'message': 'Error in fetching data from PokeAPI'})
