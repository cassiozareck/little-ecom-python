from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    owner = models.CharField(max_length=255)

    def is_owner(self, owner):
        return self.owner == owner

    def __str__(self):
        return f"{self.name} - {self.price} - {self.owner}"