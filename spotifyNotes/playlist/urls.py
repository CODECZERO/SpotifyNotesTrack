# playlist/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.spotify_login, name='spotify_login'),
    path('track/<str:track_id>/notes/', views.notes_view, name='track_notes'),
    path('track/<str:track_id>/analysis/',
         views.track_notes_analysis, name='track_notes_analysis'),
]
