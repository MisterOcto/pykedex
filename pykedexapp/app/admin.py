from django.contrib import admin

# Register your models here.
from .models import Pokemon, User, Team

admin.site.register(Pokemon)
admin.site.register(User)
admin.site.register(Team)
