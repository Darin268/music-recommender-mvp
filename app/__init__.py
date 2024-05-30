from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SPOTIPY_CLIENT_ID'] = os.getenv('SPOTIPY_CLIENT_ID')
app.config['SPOTIPY_CLIENT_SECRET'] = os.getenv('SPOTIPY_CLIENT_SECRET')
app.config['SPOTIPY_REDIRECT_URI'] = os.getenv('SPOTIPY_REDIRECT_URI')

from app import routes
