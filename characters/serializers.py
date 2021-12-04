from rest_framework import serializers

class CharacterSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=8)