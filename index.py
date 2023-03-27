from flask import Flask, render_template, request, send_file, redirect, session, url_for, after_this_request
from functions import *

app = Flask(__name__)

app.config.update(
    TESTING=True,
    TEMPLATES_AUTO_RELOAD = True,
    BASE_URL = 'http://localhost:5000/'
)

app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_COOKIE_NAME"] = "spotify-auth-session"

# Set up the SpotifyOAuth object with your app's client ID, client secret, and redirect URI
sp_oauth = SpotifyOAuth(
    client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private",
)

sp = spotipy.Spotify(auth_manager=sp_oauth)

@app.route("/")
def index():
    # Check if user is already authenticated
    if "spotify_token_info" in session:
        return render_template("index.html", show_form=True)
    else:
        # Render login button on root page
        return render_template("index.html", show_form=False)

@app.route("/login")
def login():
    # Redirect to Spotify authorization page
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback/")
def callback():
    # Handle callback from Spotify authorization page
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["spotify_token_info"] = token_info
    return redirect(url_for('index'))

@app.route('/download')
def download():
    # Get the playlist URL from the form data
    playlist_url = request.args.get('playlist_url')

    # if the playlist URL is valid, return it
    if playlist_url.startswith("https://open.spotify.com/playlist/"):
        # Download the tracks from the playlist
        download_tracks(playlist_url)

        # Get the title of the playlist
        playlist_title = get_playlist_title(sp, playlist_url)

        # Get the cover art of the playlist
        get_cover_art(sp, playlist_url)

        # Join the tracks together
        join_tracks(playlist_title)

        @after_this_request
        def remove_file(response):
            # Delete the mp3 file after the request is finished
            os.remove(playlist_title + '.mp3')
            # Return the response
            return response
        
        # Return the mixtape file
        return send_file(playlist_title + '.mp3', as_attachment=True)
    else:
        # if the playlist URL is invalid, ask the user to enter it again
        print("Invalid playlist URL. Please try again.")
        return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)