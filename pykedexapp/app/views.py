from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from rest_framework import viewsets



def home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def menu(request):
  template = loader.get_template('menu.html')
  return HttpResponse(template.render())

def signup(request):
  template = loader.get_template('signup.html')
  return HttpResponse(template.render())

def signin(request):
  template = loader.get_template('signin.html')
  return HttpResponse(template.render())

