from django.shortcuts import render
from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView

from characters.models import Character
from characters.serializers import CharacterSerializer

from .models import Match
from .serializers import MatchSerializer

import json

def stringify(obj):
	return json.dumps(obj)


def parse(json_str):
	return json.loads(json_str)


class MatchView(APIView):
	def get(self, request, *args, **kwargs):
		pass

	def post(self, request, *args, **kwargs):
		payload = parse(request.body)

		for key in payload:
			print(key, payload[key])

		return Response({
			"data": {},
			"message": "Returned payload",
			"status": 201
			})

		
