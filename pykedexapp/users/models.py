from django.db import models


# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.name