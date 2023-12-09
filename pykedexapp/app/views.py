from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from rest_framework import viewsets
from .models import Pokemon
from .serializers import PokemonSerializer


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())