from rest_framework import serializers
from .models import Pokemon


# TODO: Create a complete serializer for each model

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = "__all__"


