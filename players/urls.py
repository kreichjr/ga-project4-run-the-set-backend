from django.urls import path
from . import views

urlpatterns = [
	path('', views.PlayerView.as_view(), name='player_view')
]