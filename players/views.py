from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView

class PlayerView(APIView):
	def get(self, request, *args, **kwargs):
		test = {
			'data': 'Test'
		}
		return Response(test)

