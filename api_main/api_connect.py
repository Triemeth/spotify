import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

def get_playlist(sp):
    playlists = sp.current_user_playlists()
    playlist_data = []

    while playlists:
        for playlist in playlists["items"]:
            playlist_data.append({
                "playlist_name": playlist['name'],
                "playlist_id": playlist['id']
            })
        if playlists["next"]:
            playlists = sp.next(playlists)
        else:
            break

    playlist_df = pd.DataFrame(playlist_data)
    return playlist_df

if __name__ == "__main__":
    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),  
        scope="playlist-read-private playlist-read-collaborative"
    ))

    playlist_df = get_playlist(sp)
    print(playlist_df)


    
#py -3.12 api_main/api_connect.py