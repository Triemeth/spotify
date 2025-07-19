import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import numpy as np

def get_song_info(some_list, sp):
    return_list = []

    while some_list:
        for song in some_list['items']:
            if 'track' in song:
                name_hold = song['track']['artists'][0]['name']

                artist = sp.search(q=f"artist:{name_hold}", type="artist", limit=1)
                items = artist['artists']['items']

                if not items:
                    artist_genre = []
                else:
                    artist_info = items[0]
                    artist_genre = artist_info.get('genres', [])

                return_list.append({
                    "track_name": song['track']['name'],
                    "artist_name": name_hold,
                    "artist_genre": artist_genre,
                    "album_name": song['track']['album']['name'],
                    "release_date": song['track']['album']['release_date'],
                    "album_track_amount": song['track']['album']['total_tracks'],
                    "song_duration_minutes": song['track']['duration_ms'] * 1.66667e-5,
                    "popularity_score": song['track']['popularity'],
                    "track_number_on_album": song['track']["track_number"]
                })
            else:
                name_hold = song['artists'][0]['name']

                artist = sp.search(q=f"artist:{name_hold}", type="artist", limit=1)
                items = artist['artists']['items']

                if not items:
                    artist_genre = []
                else:
                    artist_info = items[0]
                    artist_genre = artist_info.get('genres', [])

                return_list.append({
                    "track_name": song['name'],
                    "artist_name": name_hold,
                    "artist_genre": artist_genre,
                    "album_name": song['album']['name'],
                    "release_date": song['album']['release_date'],
                    "album_track_amount": song['album']['total_tracks'],
                    "song_duration_minutes": song['duration_ms'] * 1.66667e-5,
                    "popularity_score": song['popularity'],
                    "track_number_on_album": song["track_number"]
                })
        if some_list["next"]:
            some_list = sp.next(some_list)
        else:
            break

    return_df = pd.DataFrame(return_list)
    return return_df

def get_playlists(sp):
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

def get_playlist_songs(playlists_df, sp):
    master_track_list = pd.DataFrame()

    for i in range(0, len(playlists_df)):
        curr_tracks_unparsed = sp.playlist_tracks(playlists_df.iloc[i]['playlist_id'])
        curr_track_list = get_song_info(curr_tracks_unparsed, sp)
        curr_track_list["playlist"] = playlists_df.iloc[i]['playlist_name']

        master_track_list = pd.concat([master_track_list, curr_track_list])
                    
    return master_track_list


def get_recently_listened_to(sp, limit = 20):
    recent_songs = sp.current_user_recently_played(limit=limit)
    recent_song_df = get_song_info(recent_songs, sp)

    recent_song_df["issingle"] = np.where(recent_song_df["album_track_amount"] == 1, 1, 0)

    return recent_song_df

def get_top_track_and_artists(sp, limit_artist = 5, limit_song = 10):

    short_art = []
    med_art = []
    long_art = []

    short_curr_artists = sp.current_user_top_artists(limit = limit_artist, time_range = 'short_term')
    med_curr_artists = sp.current_user_top_artists(limit = limit_artist, time_range = 'medium_term')
    long_curr_artists = sp.current_user_top_artists(limit = limit_artist, time_range = 'long_term')

    for i in range(0, 5):
        short_art.append({
            "artist_name": short_curr_artists['items'][i]["name"],
            "artist_genres": short_curr_artists["items"][i]["genres"],
            "artist_popularity": short_curr_artists["items"][i]["popularity"],
            "artist_followers": short_curr_artists["items"][i]["followers"],
        })

        med_art.append({
            "artist_name": med_curr_artists['items'][i]["name"],
            "artist_genres": med_curr_artists["items"][i]["genres"],
            "artist_popularity": med_curr_artists["items"][i]["popularity"],
            "artist_followers": med_curr_artists["items"][i]["followers"],
        })

        long_art.append({
            "artist_name": long_curr_artists['items'][i]["name"],
            "artist_genres": long_curr_artists["items"][i]["genres"],
            "artist_popularity": long_curr_artists["items"][i]["popularity"],
            "artist_followers": long_curr_artists["items"][i]["followers"],
        })

    short_art = pd.DataFrame(short_art)
    med_art = pd.DataFrame(med_art)
    long_art = pd.DataFrame(long_art)

    short_art["time_frame"] = "short"
    med_art["time_frame"] = "medium"
    long_art["time_frame"] = "long"

    artist_df = pd.concat([short_art, med_art, long_art])

    short_curr_songs = sp.current_user_top_tracks(limit = limit_song, time_range = 'short_term')
    med_curr_songs = sp.current_user_top_tracks(limit = limit_song, time_range = 'medium_term')
    long_curr_songs = sp.current_user_top_tracks(limit = limit_song, time_range = 'long_term')

    short_songs_df = get_song_info(short_curr_songs, sp)
    med_songs_df = get_song_info(med_curr_songs, sp)
    long_songs_df = get_song_info(long_curr_songs, sp)

    short_songs_df["term"] = "short"
    med_songs_df["term"] = "medium"
    long_songs_df["term"] = "long"

    top_songs = pd.concat([short_songs_df, med_songs_df, long_songs_df])

    return top_songs, artist_df
    
if __name__ == "__main__":
    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),  
        scope="playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read"
    ))

    #playlist = get_playlists(sp)
    #recent_songs = get_recently_listened_to(sp)
    #track_list = get_playlist_songs(playlist, sp)

    top_songs, top_artists = get_top_track_and_artists(sp)

    #print(top_songs.head())
    #print(recent_songs.head())
    #print(track_list.head())

    print(top_songs.head())
    print(top_artists.head())

#py -3.12 api_main/api_connect.py