# Spotify developer's dashboard (must have an account and must create an app):
# https://developer.spotify.com/dashboard/
# Spotipy module documentation:
# https://spotipy.readthedocs.io/en/2.22.1/
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy import SpotifyOAuth
from dotenv import load_dotenv
import os
# import time  # debugging. Slow down the api calls to Spotify to make it easier to track in the console.
# import pprint as pp  # debugging.


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
artists = [title.next_element.next_element.next_element.get_text().strip() for title in soup.select("li h3", limit=100)]
spotify_search_terms = list(zip(song_titles, artists))
# pp.pprint(spotify_search_terms)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_OAUTH_SCOPE
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

year = user_date.split("-")[0]
spotify_song_uris = []

for search_term in spotify_search_terms:
    # print(search_term[0], search_term[1])
    search_result = sp.search(
        q=f"{search_term[0]} {search_term[1]} {year}",
        type="track",
        limit=1
    )

    try:
        song_uri = search_result["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"Something went wrong.")
        print(f"search_term: {search_term}")
        print(search_result)
    else:
        spotify_song_uris.append(song_uri)
    # debugging.
    # time.sleep(1)
# pp.pprint(spotify_song_uris)
# print(len(spotify_song_uris))

# Debugging.
# search_term = ""
# uri = sp.search(
#     q=f"{search_term} {year}",
#     type="track",
#     limit=1
# )
# pp.pprint(uri)
# print(uri["tracks"]["items"][0]["uri"])

playlist_response = sp.user_playlist_create(
    user=user_id,
    name=f"Billboard's Hot 100 for {user_date}",
    public=False,
    collaborative=False
)
playlist_id = playlist_response["id"]
# print(playlist_response)
# print(playlist_id)

sp.playlist_add_items(
    playlist_id=playlist_id,
    items=spotify_song_uris,
)