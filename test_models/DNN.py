import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score
from ast import literal_eval
import warnings

warnings.filterwarnings("ignore")

def dnn_regression(input_shape, X_train, X_test, y_train, y_test):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_shape,)),
        Dropout(0.4),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])
    
    history, y_pred = compile_fit(model, X_train, y_train, X_test, y_test)
    return history, y_pred, model

def compile_fit(model, X_train, y_train, X_test, y_test):
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mse']
    )
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=100,
        batch_size=64,
        verbose=1
    )
    
    y_pred = model.predict(X_test)
    return history, y_pred

def getMetrics(y_pred, y_true):
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print("MSE:", mse)
    print("R2:", r2)

if __name__ == "__main__":
    load_dotenv(dotenv_path=Path(r"C:\Users\EJTri\Documents\spotify\eda\eda_with_sql.ipynb").resolve().parent.parent / ".env")

    db_user = os.getenv("POSTGRES_USER")
    db_pass = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
    all_tracks = pd.read_sql("SELECT * FROM all_tracks_saved", engine)

    all_tracks = all_tracks[all_tracks.song_duration_minutes > 0]
    all_tracks["release_date"] = all_tracks["release_date"].apply(pd.to_datetime)
    all_tracks["release_date"] = [(i - min(all_tracks["release_date"])).total_seconds() for i in all_tracks["release_date"]]

    all_tracks["artist_genre"] = all_tracks["artist_genre"].apply(literal_eval)
    all_tracks["art_genre_count"] = all_tracks["artist_genre"].apply(len)

    drop_list = ["track_name", "artist_name", "artist_genre", "album_name", "playlist"]
    all_tracks = all_tracks.drop(columns=drop_list)

    y = all_tracks["popularity_score"].values.reshape(-1, 1)
    X = all_tracks.drop(columns=["popularity_score"])

    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)

    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=19)

    history, y_pred_scaled, model = dnn_regression(X_train.shape[1], X_train, X_test, y_train, y_test)

    y_pred_unscaled = scaler_y.inverse_transform(y_pred_scaled)
    y_test_unscaled = scaler_y.inverse_transform(y_test)

    getMetrics(y_pred_unscaled, y_test_unscaled)

#py -3.12 test_models/DNN.py