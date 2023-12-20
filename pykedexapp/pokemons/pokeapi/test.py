# Importing necessary modules for testing
from django.test import TestCase
from unittest.mock import patch
import responses
from rest_framework import status
from rest_framework.test import APIClient

class PokemonAPITest(TestCase):
    def setUp(self):
        # Setup APIClient
        self.client = APIClient()

    @responses.activate
    def test_get_pokemon_by_name_success(self):
        # Mock the PokeAPI response for a specific Pokemon name
        pokemon_name = "pikachu"
        mock_response = {
            "name": "pikachu",
            "species": {"name": "pikachu"},
            "height": 4,
            "weight": 60
        }
        responses.add(
            responses.GET,
            f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}',
            json=mock_response,
            status=200
        )

        # Make a request to the endpoint
        response = self.client.get(f'/pokeapi/get/one/{pokemon_name}')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, mock_response)

    @responses.activate
    def test_get_pokemon_by_name_not_found(self):
        # Mock the PokeAPI response for a non-existing Pokemon
        pokemon_name = "unknownpokemon"
        responses.add(
            responses.GET,
            f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}',
            status=404
        )

        # Make a request to the endpoint
        response = self.client.get(f'/pokeapi/get/one/{pokemon_name}')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Additional tests can be added for edge cases, invalid inputs, and exception handling

# This is just a demonstration. Additional setup might be required depending on the project's configuration.
