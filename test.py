import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = ""
client_secret = ""

auth = spotipy.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://127.0.0.1:5000/authorize/',
            scope="user-library-read")
token = auth.get_cached_token()
sp = spotipy.Spotify(auth=token['access_token'])

#test from spotipy manual
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

