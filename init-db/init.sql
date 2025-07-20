CREATE TABLE IF NOT EXISTS all_tracks_saved(
    id SERIAL PRIMARY KEY,
    track_name TEXT,
    artist_name TEXT,
    artist_genre TEXT[],
    album_name TEXT,
    release_date DATE,
    album_track_amount INT,
    song_duration_minutes FLOAT,
    popularity_score FLOAT,
    track_number_on_album INT,
    playlist TEXT,
    Created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recent_songs(
    id SERIAL PRIMARY KEY,
    track_name TEXT,
    artist_name TEXT,
    artist_genre TEXT[],
    album_name TEXT,
    release_date DATE,
    album_track_amount INT,
    song_duration_minutes FLOAT,
    popularity_score FLOAT,
    track_number_on_album INT,
    issingle INT,
    Created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS all_tracks_saved(
    id SERIAL PRIMARY KEY,
    artist_name TEXT,
    artist_genre TEXT[],
    artist_popularity FLOAT,
    artist_followers INT,
    time_frame VARCHAR(15),
    Created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS all_tracks_saved(
    id SERIAL PRIMARY KEY,
    track_name TEXT,
    artist_name TEXT,
    artist_genre TEXT[],
    album_name TEXT,
    release_date DATE,
    album_track_amount INT,
    song_duration_minutes FLOAT,
    popularity_score FLOAT,
    track_number_on_album INT,
    term VARCHAR(15),
    Created_at TIMESTAMP DEFAULT NOW()
);