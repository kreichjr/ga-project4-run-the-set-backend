from django.shortcuts import render
from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView

from characters.models import Character
from characters.serializers import CharacterSerializer

from .models import Player
from .serializers import PlayerSerializer

import json

def stringify(obj):
	return json.dumps(obj)


def parse(json_str):
	return json.loads(json_str)


class PlayerView(APIView):
	def get(self, request, *args, **kwargs):
		all_players = Player.objects.all()

		all_players_list = []
		for player in all_players:
			all_players_list.append(PlayerSerializer(player).data)


		return Response({
			"data": all_players_list,
			"message": f"Successfully found {len(all_players_list)} players",
			"status": 200
			})


	def post(self, request, *args, **kwargs):
		payload = parse(request.body)
		print(payload)
		try:
			default_char = Character.objects.get(id=payload['default_char'])
			new_player = Player(name=payload["name"], default_char=default_char)
			new_player.save()

			data = PlayerSerializer(new_player).data

			return Response({
				"data": data,
				"message": "Player successfully created!",
				"status": 201
			})

		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "The character does not exist",
				"status": 400 
				})


class PlayerViewWithID(APIView):
	def get(self, request, pk):
		try:
			player = Player.objects.get(pk=pk)
			data = PlayerSerializer(player).data

			return Response({
				"data": data,
				"message": f"Successfully found the player {player.name}",
				"status": 200 
				})

		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "The player does not exist",
				"status": 400 
				})


	def put(self, request, pk):
		payload = parse(request.body)

		try:
			player = Player.objects.get(pk=pk)

		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "The player does not exist",
				"status": 400 
				})

		if payload.get('default_char') is not None:
			try: 
				updated_char = Character.objects.get(id=payload['default_char'])
				player.default_char = updated_char
			except models.ObjectDoesNotExist:
				return Response({
					"data": None,
					"message": "The provided character name does not match the character list",
					"status": 400 
					}) 

		player.name = payload['name']
		player.save()

		data = PlayerSerializer(player).data

		return Response({
			"data": data,
			"message": "The player was successfully updated",
			"status": 200 
			})


	def delete(self, request, pk):
		try:
			player = Player.objects.get(pk=pk)
			data = PlayerSerializer(player).data
			player.delete()

			return Response({
				"data": data,
				"message": f"The player {data['name']} was successfully deleted",
				"status": 200 
				})

		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "The player does not exist",
				"status": 400 
				})


		

