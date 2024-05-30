from flask import request, jsonify, render_template
from app import app
from app.recommender import fetch_song_features, preprocess_features, recommend_songs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    liked_song_id = data.get('liked_song_id')
    song_ids = data.get('song_ids')
    
    client_id = app.config['SPOTIPY_CLIENT_ID']
    client_secret = app.config['SPOTIPY_CLIENT_SECRET']
    
    features = fetch_song_features(song_ids, client_id, client_secret)
    features_df, numerical_features = preprocess_features(features)
    
    recommended_songs = recommend_songs(liked_song_id, features_df, numerical_features)
    return jsonify({'recommended_songs': recommended_songs})
