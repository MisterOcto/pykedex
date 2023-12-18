from . import views

urlpatterns = [
    # [GET] POKEAPI
    # The following are the endpoints for the PokeAPI
    # https://pokeapi.co/docs/v2/pokemon
    ('pokeapi/get/one/<str:name>', views.get_pokemon_from_pokeapi_by_name),
    ('pokeapi/get/one/<int:id>', views.get_pokemon_from_pokeapi_by_id),
    ('pokeapi/get/some/<int:limit>/<int:offset>', views.get_some_pokemon_from_pokeapi),
    ('pokeapi/get/some/<str:name>', views.get_some_pokemon_from_pokeapi_by_letters),
    ('pokeapi/get/all', views.get_all_pokemon_from_pokeapi),

    # [GET] API
    # The following are the endpoints for the API (pokemons saved in the database)
    ('get/all', views.get_all_pokemon),
    ('get/byteamid/<int:team_id>', views.get_pokemon_by_team_id),
    ('get/byuserid/<int:user_id>/', views.get_pokemon_by_user_id),

    # [POST] API
    # Pokemons are saved because they are on a team
    ('post/in_this_team/<int:team_id>', views.post_pokemon),

    # [PUT] API
    # Pokemons stats might change
    ('put/<int:id>', views.put_pokemon),

    # [DELETE] API
    # Pokemons are deleted because they are removed from a team
    ('delete/<int:id>', views.delete_pokemon),
]
