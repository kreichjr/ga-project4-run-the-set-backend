from django.db import models

class Player(models.Model):
	name = models.CharField(max_length=64)
	default_char = models.CharField(max_length=8)
