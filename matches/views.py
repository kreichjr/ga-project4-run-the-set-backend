from django.shortcuts import render
from django.db import models
from django.db.models import Q

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
		if payload['player_1'] == payload['player_2']:
			return Response({
				"data": None,
				"message": "Player 1 and Player 2 cannot be the same",
				"status": 400
				})

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
	def get(self, request, id):
		try:
			match = Match.objects.get(id=id)
		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "Unable to get match - Match ID does not exist",
				"status": 400
				})

		data = MatchSerializer(match).data

		return Response({
				"data": data,
				"message": f"Successfully returned match id {id}",
				"status": 200
				})


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


class MatchFilterViewWithID(APIView):
	def get(self, request, id):
		try:
			player = Player.objects.get(id=id)
			
		except models.ObjectDoesNotExist:
			return Response({
				"data": None,
				"message": "Error",
				"status": 400
				})

		char_id     = request.GET.get('char', None)
		opponent_id = request.GET.get('opponent', None)
		played_char = None
		opponent    = None

		p1_query = Q(player_1__exact=id)
		p2_query = Q(player_2__exact=id)

		if char_id:
			try:
				played_char = Character.objects.get(id=char_id)
			except models.ObjectDoesNotExist:
				played_char = None

			p1_query = p1_query & Q(p1_char__exact=char_id)
			p2_query = p2_query & Q(p2_char__exact=char_id)

		if opponent_id:
			try:
				opponent = Player.objects.get(id=opponent_id)
			except models.ObjectDoesNotExist as e:
				opponent = None

			p1_query = p1_query & Q(player_2__exact=opponent_id)
			p2_query = p2_query & Q(player_1__exact=opponent_id)
			
		
		p1_matches = Match.objects.filter(p1_query)
		p2_matches = Match.objects.filter(p2_query)
		p1_won_match_count = 0
		p2_won_match_count = 0

		for match in p1_matches:
			p1_won_match_count = p1_won_match_count + 1 if match.p1_is_winner else p1_won_match_count
		for match in p2_matches:
			p2_won_match_count = p2_won_match_count + 1 if not match.p1_is_winner else p2_won_match_count
		
		match_list = [MatchSerializer(p1_match).data for p1_match in p1_matches] + [MatchSerializer(p2_match).data for p2_match in p2_matches]
		match_count = len(match_list)
		won_match_count = p1_won_match_count + p2_won_match_count

		data = {
			"matches": match_list,
			"won_matches": won_match_count,
			"total_matches": match_count
		}

		message = f'Successfully returned {match_count} matches for {player.name}'
		if played_char is not None:
			message = message + f' as {played_char.name}'
		if opponent is not None:
			message = message + f' against {opponent.name}' if opponent is not None else message

		return Response({
			"data": data,
			"message": message,
			"status": 200
			})










