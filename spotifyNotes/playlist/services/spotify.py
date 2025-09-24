import os
import requests
from urllib.parse import urlencode

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_SCOPES = "user-top-read playlist-read-private"


class SpotifyService:
    def __init__(self, session):
        """
        session: Django request.session
        """
        self.session = session
        self.access_token = session.get("spotify_token")

    # 1️⃣ Generate Spotify login URL
    @staticmethod
    def get_login_url():
        params = {
            "response_type": "code",
            "client_id": SPOTIFY_CLIENT_ID,
            "scope": SPOTIFY_SCOPES,
            "redirect_uri": SPOTIFY_REDIRECT_URI,
        }
        return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

    # 2️⃣ Exchange authorization code for access token
    def exchange_code_for_token(self, code):
        token_url = "https://accounts.spotify.com/api/token"
        response = requests.post(token_url, data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET
        })

        data = response.json()
        self.access_token = data.get("access_token")
        self.session["spotify_token"] = self.access_token
        return self.access_token

    def get_top_tracks(self, limit=20, time_range="medium_term"):
        if not self.access_token:
            return []

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"https://api.spotify.com/v1/me/top/tracks?limit={limit}&time_range={time_range}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("items", [])
        return []

    def get_user_playlists(self, limit=20):
        if not self.access_token:
            return []

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"https://api.spotify.com/v1/me/playlists?limit={limit}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("items", [])
        return []

    def get_user_profile(self):
        if not self.access_token:
            return {}

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = "https://api.spotify.com/v1/me"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}
