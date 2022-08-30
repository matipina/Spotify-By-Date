from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secret_key import create_key, client_id, client_secret
import os

app = Flask(__name__)


app.secret_key = create_key()
app.config['SESSION_COOKIE_NAME'] = 'SpotiCookie'


@app.route('/')
def login():
    spotify_oauth = create_spotify_oauth()
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    return 'Authorized!'


@app.route('/getTracks')
def getTracks():
    return 'Some songs'


@app.route('/getAlbums')
def getAlbums():
    return 'Some cool albums'


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('authorize', _external=True),
        scope='user-library-read'
    )


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)