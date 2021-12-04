from rest_framework import serializers

class CharacterSerializer(serializers.Serializer):
	id = serializers.ReadOnlyField()
	name = serializers.CharField(max_length=8)