import pandas as pd
from get_top_and_recent import get_song_info, env_loading_stuff
import json

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

if __name__ == "__main__":
    sp, engine = env_loading_stuff()

    playlist = get_playlists(sp)
    track_list = get_playlist_songs(playlist, sp)

    track_list["artist_genre"] = track_list["artist_genre"].apply(json.dumps)

    track_list.to_sql("all_tracks_saved", engine, if_exists="replace", index=False)

#py -3.12 api_main/get_all_tracks.py