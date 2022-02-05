from io import BytesIO
from PIL import Image
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import requests
import time
import sys
import json
import os

def load_config():
    if not os.path.isfile("config.json"):
        config = json.dumps({"client_id" : "", "client_secret" : "", "redirect_uri" : ""}, indent=4)
        with open("config.json", "w") as outfile:
            outfile.write(config)
    else:
        with open("config.json") as file:
            config = json.load(file)
    return config

def get_album_cover_url():
    result = sp.current_user_playing_track()
    imageURL = result["item"]["album"]["images"][0]["url"]
    return imageURL

if __name__ == '__main__':

    config = load_config()

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']

    if not client_id or not client_secret or not redirect_uri:
        print('Fill in config.json')
        sys.exit(0)

    scope = 'user-read-currently-playing'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

    currentSong = ''
    prevSong = ''

    try:
        while 1:
            try:
                imageUrl = get_album_cover_url()
                currentSong = imageUrl

                if prevSong != currentSong:
                    response = requests.get(imageUrl)
                    image = Image.open(BytesIO(response.content))
                    image = image.save('cover.png')
                    prevSong = currentSong
                
                time.sleep(1)
            except Exception as e:
                print('Failed to get song')
                time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)
