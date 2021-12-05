from rest_framework import serializers

from characters.serializers import CharacterSerializer
from players.serializers import PlayerSerializer

from characters.models import Character
from players.models import Player

class MatchSerializer(serializers.Serializer):
	id = serializers.ReadOnlyField()
	player_1 = PlayerSerializer(Player)
	player_2 = PlayerSerializer(Player)
	p1_char = CharacterSerializer(Character)
	p2_char = CharacterSerializer(Character)
	p1_rounds_won = serializers.IntegerField()
	p2_rounds_won = serializers.IntegerField()
	p1_is_winner = serializers.BooleanField()
	createdAt = serializers.DateTimeField()

