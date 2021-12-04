from django.db import models
from characters.models import Character
from players.models import Player

from characters.serializers import CharacterSerializer
from players.serializers import PlayerSerializer

import datetime

class Match(models.Model):
	player_1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name="matches_as_p1")
	player_2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name="matches_as_p2")
	p1_char = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="as_p1")
	p2_char = models.ForeignKey(Character, null=True, on_delete=models.SET_NULL, related_name="as_p2")
	p1_rounds_won = models.IntegerField()
	p2_rounds_won = models.IntegerField()
	p1_is_winner = models.BooleanField()
	createdAt = models.DateTimeField(default=datetime.datetime.now)

	def __str__(self):
		p1 = PlayerSerializer(self.player_1).data['name']
		return p1

