from django.shortcuts import render, redirect
from .db.db_queries import select_notes
from .services.analytics import analyze_notes_sentiment,plot_sentiment_distribution
from .services.spotify import SpotifyService
# Create your views here.

def track_notes_analysis(request, trackId):
    userId = request.session.get("spotify_user_id")
    if not userId:
        return redirect("spotify_login")
    #fetch data from db
    notes = select_notes(trackId)
    
    sentiment_counts, analyzed_notes = analyze_notes_sentiment(notes)
    chart_html = plot_sentiment_distribution(sentiment_counts)
    
    return render(request, "playlist/track_notes_analysis.html",{
        "chart_html": chart_html,
        "analyzed_notes": analyzed_notes,
        "track_id": trackId
    })
    
def spotify_login(request):
    loginUrl=SpotifyService.get_login_url()
    return redirect(loginUrl)

def spotify_callback(request):
    code=request.GET.get("code")
    if not code:
        return redirect("spoify_login")
    
    service=SpotifyService(request.session)
    service.exchange_code_for_token(code)
    
    profile=service.get_user_profile()
    request.session["spotify_user_id"] = profile.get("id")
    return redirect("dashboard")

def dashboard(request):
    service=SpotifyService(request.session)
    tracks=service.get_top_tracks()
    playlists=service.get_user_playlists()
    return render(request,"playlists/dashboard.html",{"tracks": tracks,"playlist": playlists })
