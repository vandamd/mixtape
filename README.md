# Mixtape

A simple, mixtape generator for your Spotify playlists. 
- Order is respected
- Playlist titles and covers are transferred
- Songs are in 128kbps MP3 format

## Installation

1. Clone the repository:
    
    `git clone https://github.com/vandamd/mixtape.git`
2. Install dependencies:

    `pip install -r requirements.txt`
3. Install [FFmpeg](https://ffmpeg.org/download.html):

    `brew install ffmpeg`

3. Create a Spotify app at https://developer.spotify.com/dashboard/applications.
4. Add your Spotify app's client ID, client secret and redirect URI to `.env`.

5. Add a Flask secret key to `.env`. You can generate one with:  

    `pwgen -s 64 1`
6. Run the app:
    
    `flask --app index.py run`

## Usage
1. Login to Spotify.
2. Copy a Spotify playlist URL.
3. Paste the URL into the input field and press Enter.
4. Wait for the mixtape to be generated. (You can check the progress in the terminal.)
5. The mixtape will be downloaded automatically.

## Demo
![Demo](demo.gif)

## Disclaimer
This project is for educational purposes only. I do not condone the use of this project for illegal purposes.