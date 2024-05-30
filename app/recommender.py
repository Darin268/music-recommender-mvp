import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def fetch_song_features(song_ids, client_id, client_secret):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    features = []
    for song_id in song_ids:
        features.append(sp.audio_features(song_id)[0])
    
    return features

def preprocess_features(features):
    df = pd.DataFrame(features)
    numerical_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    scaler = StandardScaler()
    df[numerical_features] = scaler.fit_transform(df[numerical_features])
    return df, numerical_features

def recommend_songs(liked_song_id, features_df, numerical_features, top_n=10):
    similarity_matrix = cosine_similarity(features_df[numerical_features])
    idx = features_df.index[features_df['id'] == liked_song_id].tolist()[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_songs = [features_df.iloc[i[0]]['id'] for i in sim_scores[1:top_n+1]]
    return top_songs

# Example usage of SpotifyOAuth if needed
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="user-library-read"
    )
