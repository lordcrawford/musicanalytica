import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# CREATES A MORE INTUITIVE QUEUE ON EXECUTION FOR USER

client_id = ""
client_secret = ""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:5000/authorize/',
                                               scope="user-top-read"))
sp2 = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:5000/authorize/',
                                               scope="user-modify-playback-state"))
sp3 = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:5000/authorize/',
                                               scope="user-library-read"))

#gets top user tracks from recent term, medium, and old
short_term = sp.current_user_top_tracks(limit=15, time_range='short_term')
medium_term = sp.current_user_top_tracks(limit=5, time_range='medium_term')
long_term = sp.current_user_top_tracks(limit=10, time_range='long_term')

queue_songs = []
for song in short_term['items']:
    if song['uri'] not in queue_songs:
        track = song['name']
        queue_songs.append(song['uri'])

for song in medium_term['items']:
    if song['uri'] not in queue_songs:
        track = song['name']
        queue_songs.append(song['uri'])

max_old_count = 0
for song in long_term['items']:
    if song['uri'] not in queue_songs and max_old_count < 5:
        track = song['name']
        queue_songs.append(song['uri'])
        max_old_count += 1

#fetches recommendations based on most recently top played songs
recs = sp.recommendations(seed_tracks=queue_songs[0:5], limit=30)
for rec in recs['tracks']:
    if rec['uri'] not in queue_songs:
        track = rec['name']
        queue_songs.append(rec['uri'])
        print(track)

#creates new queue
random.shuffle(queue_songs)
sp2.start_playback(uris=queue_songs)