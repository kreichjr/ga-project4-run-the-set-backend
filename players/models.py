from django.db import models
from characters.models import Character

class Player(models.Model):
	name = models.CharField(max_length=64)
	default_char = models.ForeignKey(Character, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


