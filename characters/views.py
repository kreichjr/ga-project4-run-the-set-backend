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

		all_chars_list = []
		for char in all_chars:
			serialized_data = CharacterSerializer(char)
			all_chars_list.append(serialized_data.data)
		
		print('Here\'s all the chars')
		print(all_chars_list)


		return Response({"data": all_chars_list})


# class CharacterSeedView(APIView):
# 	def get(self, request, *args, **kwargs):
# 		all_chars = Character.objects.all()

# 		all_chars_list = []
# 		for char in all_chars:
# 			serialized_data = CharacterSerializer(char)
# 			all_chars_list.append(serialized_data.data)
		
# 		print('Here\'s all the chars')
# 		print(all_chars_list)


# 		return Response({"data": all_chars_list})

# 	def post(self, request, *args, **kwargs):
# 		# for character in character_list:
# 		# 	new_char = Character(name=character)
# 		# 	new_char.save()

# 		# all_chars = Character.objects.all()
# 		print(json.loads(request.body))
# 		return Response(request.body)

