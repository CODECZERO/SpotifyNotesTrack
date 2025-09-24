# playlist/urls.py
from django.urls import path
from . import views
app_name = 'playlist'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.spotify_login, name='spotify_login'),
    path('callback/', views.spotify_callback, name='spotify_callback'),
    path('track/<str:track_id>/notes/', views.notes_view, name='track_notes'),
    path('track/<str:track_id>/analysis/',
         views.track_notes_analysis, name='track_notes_analysis'),
    path('track/<str:track_id>/note/',
         views.add_or_update_note, name='add_or_update_note'),
]
