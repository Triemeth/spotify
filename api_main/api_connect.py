import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv('/app/.env')

    cli = os.getenv("CLIENT_ID")
    secret = os.getenv("CLIENT_SECRET")

    print(cli)
    print(secret)

    """client_credentials_manger = SpotifyClientCredentials(client_id = cli,
                                                        client_secret = secret)
    
    sp = spotipy.Spotify(client_credentials_manger = client_credentials_manger)

    playlists = sp.user_playlists('spotify')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(f"{i + 1 + playlists['offset']:4d} {playlist['uri']} {playlist['name']}")
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None"""

#py -3.12 api_main/api_connect.py