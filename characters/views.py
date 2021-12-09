from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CharacterSerializer
from .models import Character 
import json

character_list = [
			'Akuma',
			'Urien',
			'Necro',
			'Ibuki',
			'Sean',
			'Alex',
			'Yun',
			'Remy',
			'Q',
			'Chun Li',
			'Makoto',
			'Twelve',
			'Yang',
			'Ryu',
			'Oro',
			'Dudley',
			'Elena',
			'Hugo',
			'Ken'
		]


class CharacterView(APIView):
	def get(self, request, *args, **kwargs):
		all_chars = Character.objects.all()
		all_chars_dict = {}

		for char in all_chars:
			serialized_data = CharacterSerializer(char)

			all_chars_dict[serialized_data.data['id']] = serialized_data.data['name']
		
		return Response({
			"data": all_chars_dict,
			"message": f"Successfully found {len(all_chars_dict)} characters",
			"status": 200
			})


class CharacterSeedView(APIView):
	def post(self, request, *args, **kwargs):
		db_chars = Character.objects.all()
		if len(db_chars) == 19:
			return Response({
				"data": None,
				"message": f"No seeding performed, characters already exist",
				"status": 200
				})

		all_chars_data = []

		for character in character_list:
			new_char = Character(name=character)
			new_char.save()
			all_chars_data.append(CharacterSerializer(new_char).data)

		return Response({
			"data": all_chars_data,
			"message": f"Successfully created {len(all_chars_data)} characters",
			"status": 200
			})

