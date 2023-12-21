# Spotify developer's dashboard (must have an account):
# https://developer.spotify.com/dashboard/
# Spotipy module documentation:
# https://spotipy.readthedocs.io/en/2.22.1/
import requests
import spotipy
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(".env")
BILLBOARD_HOT_100_URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_OAUTH_SCOPE = "playlist-modify-private"

user_date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD format:\n")
response = requests.get(url=f"{BILLBOARD_HOT_100_URL}{user_date}")
response.raise_for_status()
billboard_content = response.text
soup = BeautifulSoup(billboard_content, "html.parser")
song_titles = [title.get_text().strip() for title in soup.select("li h3", limit=100)]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_OAUTH_SCOPE
    )
)
user_id = sp.current_user()["id"]
print(user_id)
