ALTER TABLE all_tracks_saved
ALTER COLUMN artist_genre TYPE TEXT;

ALTER TABLE recent_songs
ALTER COLUMN artist_genre TYPE TEXT;

ALTER TABLE top_artists
ALTER COLUMN artist_genre TYPE TEXT;

ALTER TABLE top_songs
ALTER COLUMN artist_genre TYPE TEXT;
