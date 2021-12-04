from django.urls import path
from . import views

urlpatterns = [
	path('', views.MatchView.as_view(), name="match_view")
	]