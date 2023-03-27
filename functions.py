import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from dotenv import load_dotenv

# Set up the Spotify object with the access token
def get_spotify(access_token):
    return spotipy.Spotify(auth=access_token)

# # Ask user for Spotify Playlist URL
# def get_playlist_url():
#     playlist_url = input("Enter the URL of the playlist you want to download: ")

#     # if the playlist URL is valid, return it
#     if playlist_url.startswith("https://open.spotify.com/playlist/"):
#         return playlist_url
#     else:  
#         # if the playlist URL is invalid, ask the user to enter it again
#         print("Invalid playlist URL. Please try again.")
#         get_playlist_url()

# Download the tracks with spotdl
def download_tracks(playlist_url):
    # Create a directory called `mixtape` to store the tracks
    os.system("mkdir mixtape")

    # cd into the directory where the tracks will be downloaded
    os.chdir("mixtape")

    # Download the tracks with with `spotdl download [playlistUrl]` with bitrate disabled and numbered in order
    os.system("spotdl --bitrate disable --output '{list-position}' download " + playlist_url)

    # Generate a tracks.txt of the tracks in the `mixtape' directory
    # in the form of 'file '/path/to/1.mp3''
    os.system("ls -1 *.mp3 | sed 's/^/file /' > tracks.txt")

    # remove the last line of the tracks.txt file
    os.system("sed -i '$ d' tracks.txt")

    # cd back to the root directory
    os.chdir("..")

# Get the cover art of the playlist
def get_cover_art(sp, playlist_url):
    # Get the playlist ID from the URL
    playlist_id = playlist_url.split("/")[4]

    # remove the `?si=` part of the playlist ID
    playlist_id = playlist_id.split("?")[0]

    # Get the playlist cover art
    playlist_cover = sp.playlist_cover_image(playlist_id)

    # Read the 'url' key of the playlist cover art
    playlist_cover_url = playlist_cover[0]['url']

    # Download the playlist cover art
    response = requests.get(playlist_cover_url)
    if response.status_code == 200:
        with open('playlist_cover.jpg', 'wb') as f:
            f.write(response.content)
    else:
        print('Failed to download playlist cover art')

# Get the title of the playlist
def get_playlist_title(sp, playlist_url):
    # Get the playlist ID from the URL
    playlist_id = playlist_url.split("/")[4]

    # remove the `?si=` part of the playlist ID
    playlist_id = playlist_id.split("?")[0]

    # Get the playlist title
    playlist_title = sp.playlist(playlist_id)['name']

    # If the title has an apostrophe, delete it
    playlist_title = playlist_title.replace("'", "")

    return playlist_title

# Join the tracks together with ffmpeg
def join_tracks(title):
    # Look at the tracks.txt file and join the tracks together
    os.system("ffmpeg -f concat -safe 0 -i mixtape/tracks.txt -c copy mixtape.mp3")

    # Add the cover art to the joined tracks
    os.system("ffmpeg -i mixtape.mp3 -i playlist_cover.jpg -c copy -map 0 -map 1 output.mp3")

    # Rename the output file to the name of the original file to overwrite it
    os.system("mv output.mp3 mixtape.mp3")

    # Remove the mixtape directory
    os.system("rm -rf mixtape")

    # Remove the playlist cover art
    os.system("rm playlist_cover.jpg")

    # Rename the mixtape file to the name of the playlist
    os.system("mv mixtape.mp3 '" + title + "'.mp3")