from rest_framework import serializers
from characters.serializers import CharacterSerializer
from characters.models import Character

class PlayerSerializer(serializers.Serializer):
	id = serializers.ReadOnlyField()
	name = serializers.CharField(max_length=64)
	default_char = CharacterSerializer(Character)