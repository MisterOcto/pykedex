from django.db import models


# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    type1 = models.CharField(max_length=30)
    type2 = models.CharField(max_length=30)

    def __str__(self):
        return self.name
