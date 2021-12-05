from django.urls import path
from . import views

urlpatterns = [
	path('', views.PlayerView.as_view(), name='player_view'),
	path('<int:pk>', views.PlayerViewWithID.as_view(), name='player_view_with_id')
]