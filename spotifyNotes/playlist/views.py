from django.shortcuts import render, redirect
from .db.db_queries import select_notes
from .services.analytics import analyze_notes_sentiment,plot_sentiment_distribution
    
# Create your views here.

def track_notes_analysis(request, trackId):
    userId = request.session.get("spotify_user_id")
    if not userId
    #fetch data from db
    notes = select_notes(trackId)