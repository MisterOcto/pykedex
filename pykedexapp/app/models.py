from django.db import models


# Create your models here.
class Pokemon(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.IntegerField()
    name = models.CharField(max_length=30)
    lvl = models.IntegerField()
    xp = models.IntegerField()
    number = models.IntegerField()
    type_1 = models.CharField(max_length=30)
    type_2 = models.CharField(max_length=30)
    special_capacity = models.CharField(max_length=30)
    memo = models.CharField(max_length=30)
    atck = models.IntegerField()
    defs = models.IntegerField()
    atck_spe = models.IntegerField()
    defs_spe = models.IntegerField()
    speed = models.IntegerField()
    hp = models.IntegerField()
    team_id = models.IntegerField()

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    user_id = models.IntegerField()

    def __str__(self):
        return self.name

