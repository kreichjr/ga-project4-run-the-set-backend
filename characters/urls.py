from django.urls import path
from . import views

urlpatterns = [
	path('', views.CharacterView.as_view(), name='character_view'),
	path('seed', views.CharacterSeedView.as_view(), name='character_seed_view')
]