from django.urls import path
from . import views

urlpatterns = [
	path('', views.MatchView.as_view(), name="match_view"),
	path('<int:id>', views.MatchViewWithID.as_view(), name="match_view_with_id")
	]