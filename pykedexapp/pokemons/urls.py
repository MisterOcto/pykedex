from . import views

urlpatterns = [
    ('pokeapi/get/<str:name>', views.get_pokemon_from_pokeapi_by_name),
    ('pokeapi/get/<int:id>', views.get_pokemon_from_pokeapi_by_id),
    ('pokeapi/get/all', views.get_all_pokemon_from_pokeapi),
    ('pokeapi/get/some/<int:limit>/<int:offset>', views.get_some_pokemon_from_pokeapi),
    ('pokeapi/get/
    ]