import time
import spotipy
from flask import Flask, request, url_for, session, redirect, render_template
from spotipy.oauth2 import SpotifyOAuth
from secret_key import create_key, client_id, client_secret
from functions import get_saved_albums, display_results
from front import DateForm

app = Flask(__name__)


app.secret_key = create_key()
app.config['SESSION_COOKIE_NAME'] = 'SpotiCookie'
TOKEN_INFO = 'token_info'
year = '2011'


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('authorize', _external=True),
        scope='user-library-read'
    )

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"

    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info 

# Routes
@app.route('/')
def login():
    spotify_oauth = create_spotify_oauth()
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    spotify_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = spotify_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info

    return redirect(url_for('home', _external=True))


@app.route('/home/')
def home():
    return render_template('index.html')    
    #return redirect(url_for('get_tracks', _external=True),)


@app.route('/pickDate/')
def pick_date():
    form = DateForm()
    return render_template('post.html', form=form)


@app.route('/getTracks/')
def get_tracks():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        return redirect(url_for('login', _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    print(f'sp: {sp}')
    return sp.current_user_saved_tracks()['items']


@app.route('/getAlbums/')
def get_albums():
    try:
        token_info = get_token()
    except:
        print('user not logged in')
        redirect(url_for('login', _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    print(f'sp: {sp}')
    albums = get_saved_albums(sp=sp)

    if year:
        filtered_albums = [item for item in albums if item['album']['release_date'][:4] == year]
        results = display_results(filtered_albums)
 
    else:
        results = display_results(albums)

    return results


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)