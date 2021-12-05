from django.shortcuts import render
from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView

from characters.models import Character
from characters.serializers import CharacterSerializer

from players.models import Player
from players.serializers import PlayerSerializer

from .models import Match
from .serializers import MatchSerializer

import json

def stringify(obj):
	return json.dumps(obj)


def parse(json_str):
	return json.loads(json_str)


def payload_parse(payload):
	new_payload = {}

	for key, value in payload.items():
		if key == 'player_1' or key == 'player_2':
			try:
				new_payload[key] = Player.objects.get(id=value)
				continue
			except models.ObjectDoesNotExist:
				raise Exception(f"Error --- ID: {value} for Key: {key} was not found")
				

		if key == 'p1_char' or key == 'p2_char':
			try:
				new_payload[key] = Character.objects.get(id=value)
				continue
			except models.ObjectDoesNotExist:
				raise Exception(f'Error --- ID: {value} for Key: {key} was not found')

		if key in ['p1_rounds_won', 'p2_rounds_won', 'p1_is_winner']:
			new_payload[key] = payload[key]

	return new_payload


def update_match(match, payload):
	match.player_1 = payload['player_1'] if 'player_1' in payload else match.player_1
	match.player_2 = payload['player_2'] if 'player_2' in payload else match.player_2
	match.p1_char = payload['p1_char'] if 'p1_char' in payload else match.p1_char
	match.p2_char = payload['p2_char'] if 'p2_char' in payload else match.p2_char
	match.p1_rounds_won = payload['p1_rounds_won'] if 'p1_rounds_won' in payload else match.p1_rounds_won
	match.p2_rounds_won = payload['p2_rounds_won'] if 'p2_rounds_won' in payload else match.p2_rounds_won
	match.p1_is_winner = payload['p1_is_winner'] if 'p1_is_winner' in payload else match.p1_is_winner
	match.save()


class MatchView(APIView):
	def get(self, request, *args, **kwargs):
		all_matches = Match.objects.all()

		all_matches_data = [MatchSerializer(match).data for match in all_matches]

		return Response({
			"data": all_matches_data,
			"message": f"Successfully found {len(all_matches_data)} matches",
			"status": 200
			})


	def post(self, request, *args, **kwargs):
		payload = parse(request.body)

		try:
			player_1 = Player.objects.get(id=payload['player_1'])
		except models.ObjectDoesNotExist:
			return Response({
			"data": None,
			"message": "Selected Player 1 does not exist in the database",
			"status": 400
			})
		
		try:
			player_2 = Player.objects.get(id=payload['player_2'])
		except models.ObjectDoesNotExist:
			return Response({
			"data": None,
			"message": "Selected Player 2 does not exist in the database",
			"status": 400
			})

		try:
			p1_char = Character.objects.get(id=payload['p1_char'])
		except models.ObjectDoesNotExist:
			p1_char = player_1.default_char

		try:
			p2_char = Character.objects.get(id=payload['p2_char'])
		except models.ObjectDoesNotExist:
			p2_char = player_2.default_char		

		p1_rounds_won = payload['p1_rounds_won']
		p2_rounds_won = payload['p2_rounds_won']
		p1_is_winner = payload['p1_is_winner']

		new_match = Match(
				player_1=player_1,
				player_2=player_2,
				p1_char=p1_char,
				p2_char=p2_char,
				p1_rounds_won=payload['p1_rounds_won'],
				p2_rounds_won=payload['p2_rounds_won'],
				p1_is_winner=payload['p1_is_winner']
				)

		new_match.save()
		data = MatchSerializer(new_match).data

		return Response({
			"data": data,
			"message": "Successfully Created New Match",
			"status": 201
			})

		
class MatchViewWithID(APIView):
	def put(self, request, id):
		payload = parse(request.body)

		try: 
			new_payload = payload_parse(payload)

		except Exception as error:
			return Response({
				"data": None,
				"message": repr(error),
				"status": 400
				})
		
		try:
			match_to_update = Match.objects.get(id=id)

		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "Unable to update match - Match ID does not exist",
				"status": 400
				})

		update_match(match_to_update, new_payload)
		data = MatchSerializer(match_to_update).data

		return Response({
			"data": data,
			"message": "The match was updated successfully",
			"status": 200 
			})


	def delete(self, request, id):
		try:
			match_to_delete = Match.objects.get(id=id)
			data = MatchSerializer(match_to_delete).data
			match_to_delete.delete()
			
			return Response({
				"data": data,
				"message": "The match was deleted successfully",
				"status": 200 
				})

		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "Unable to delete match - Match ID does not exist",
				"status": 400
				})













