import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import random
import os

# RECOMMENDS TRULY NEW ARTISTS BASED ON PAST LISTENING HISTORY

client_id = os.environ.get('MA_CLIENT_ID')
client_secret = os.environ.get('MA_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:5000/authorize/',
                                               scope="user-top-read"))

sp2 = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:5000/authorize/',
                                               scope="user-library-read"))

#GETS TOP ARTISTS USER LISTENS TO (mostly short term)
top_recent_artists = sp.current_user_top_artists(limit=3, time_range="short_term")
top_long_artists = sp.current_user_top_artists(limit=5, time_range="long_term")

top_artist_uris = []
for artist in top_recent_artists['items']:
    if artist['uri'] not in top_artist_uris:
        track = artist['name']
        top_artist_uris.append(artist['uri'])

max_long_artists = 0
for artist in top_long_artists['items']:
    if artist['uri'] not in top_artist_uris and max_long_artists < 2:
        track = artist['name']
        top_artist_uris.append(artist['uri'])
        max_long_artists += 1

def get_all_saved_artists():
    saved_artists = []

    iter = 0
    offset = 0
    while True:
        iter_songs = sp2.current_user_saved_tracks(limit=50, offset=offset)['items']
        offset = iter * 50
        iter += 1
        for song in iter_songs:
            artist_uri = song['track']['artists'][0]['uri']
            if song['track']['artists'][0]['uri'] not in saved_artists:
                saved_artists.append(song['track']['artists'][0]['uri'])
        if len(iter_songs) < 50:
            break
    return saved_artists

def get_new_related_artists():
    new_related_artists = []
    saved_artists = get_all_saved_artists()
    for artist in top_artist_uris:
        related_request = sp.artist_related_artists(artist)
        new_related_group = []
        for related_artist in related_request['artists']:
            #pick a random artist out of each related request to add to the total list
            if related_artist['uri'] not in saved_artists:
                new_related_group.append(related_artist['name'])

        random.shuffle(new_related_group)
        new_related_artists.append(new_related_group[0])

    return new_related_artists

if __name__ == "__main__":
    print("Based on your listening history and artists you currently do not have saved, we recommend these 5 artists:\n" )
    recommended_artists = get_new_related_artists()
    for idx,item in enumerate(recommended_artists):
        print(idx+1,item)
