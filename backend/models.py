from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    owner = models.CharField(max_length=255)

    def is_owner(self, owner):
        return self.owner == owner

    def clean(self):
        if self.price < 0:
            raise ValidationError('Price cannot be negative')
        if self.name == '':
            raise ValidationError('Name cannot be empty')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'owner': self.owner
        }
    
    def __str__(self):
        return f"{self.name} - {self.price} - {self.owner}"