from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .db.db_queries import select_notes, delete_notes, upsert_notes
from .services.analytics import analyze_notes_sentiment, plot_sentiment_distribution
from .services.spotify import SpotifyService
# Create your views here.


def track_notes_analysis(request, track_id):
    userId = request.session.get("spotify_user_id")
    if not userId:
        return redirect("playlist:spotify_login")
    # fetch data from db
    notes = select_notes(trackId=track_id)

    sentiment_counts, analyzed_notes = analyze_notes_sentiment(notes)
    chart_html = plot_sentiment_distribution(sentiment_counts)

    return render(request, "playlist:dashboard/track_notes_analysis.html", {
        "chart_html": chart_html,
        "analyzed_notes": analyzed_notes,
        "track_id": track_id
    })


def spotify_login(request):
    loginUrl = SpotifyService.get_login_url()
    return redirect(loginUrl)


def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("playlist:spoify_login")

    service = SpotifyService(request.session)
    service.exchange_code_for_token(code)

    profile = service.get_user_profile()
    request.session["spotify_user_id"] = profile.get("id")
    return redirect("playlist:dashboard")


def dashboard(request):
    service = SpotifyService(request.session)
    tracks = service.get_top_tracks()
    playlists = service.get_user_playlists()
    return render(request, "dashboard/index.html", {"tracks": tracks, "playlist": playlists})


def notes_view(request, track_id):
    user_id = request.session.get("spotify_user_id")
    if not user_id:
        # redirect if user not logged in
        return redirect("playlist:spotify_login")

    # Fetch notes for this user and track
    notes = select_notes(trackId=track_id)
    # notes = list of tuples: [(Id, userId, trackId, notesText, created_at, updated_at), ...]

    return render(request, "dashboard/notes.html", {
        "notes": notes,
        "track_id": track_id
    })


@require_http_methods(["POST"])
def add_or_update_note(request, track_id):
    user_id = request.session.get("spotify_user_id")
    if not user_id:
        return redirect("playlist:spotify_login")

    note_text = request.POST.get("note_text")

    if track_id and note_text is not None:
        # upsert handles insert or update
        upsert_notes(userId=user_id, trackId=track_id, notesText=note_text)

    return redirect("playlist:track_notes", track_id=track_id)


@require_http_methods(["POST"])
def remove_note(request, track_id):
    user_id = request.session.get("playlist:spotify_user_id")
    if not user_id:
        return redirect("playlist:spotify_login")

    track_id = request.POST.get("track_id")
    if track_id:
        delete_notes(userId=user_id, trackId=track_id)

    return redirect("playlist:track_notes", track_id=track_id)