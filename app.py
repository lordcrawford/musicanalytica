import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, redirect
import os

#BOILERPLATE

app = Flask(__name__)

client_id = os.environ.get('MA_CLIENT_ID')
client_secret = os.environ.get('MA_CLIENT_SECRET')

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    return 'auth'

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=url_for('authorize', _external=True),
            scope="")