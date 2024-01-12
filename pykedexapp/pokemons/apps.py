from django.apps import AppConfig
from .task import cache_all_pokemon_data


class PokemonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pokemons"
    def ready(self):
        cache_all_pokemon_data()
