import spotipy
import API_KEY
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state app-remote-control user-modify-playback-state playlist-read-private user-follow-modify playlist-read-collaborative user-follow-read user-read-currently-playing user-read-playback-position user-library-modify playlist-modify-private playlist-modify-public user-read-email user-top-read streaming user-read-recently-played user-read-private user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=API_KEY.spotify_clientID, client_secret=API_KEY.spotify_clientSecret, redirect_uri=API_KEY.spotify_redirectURI, scope=scope))


def spotify_add_to_queue(uri):
    """
    Adds a song to the end of a user’s queue
    :param uri: Spotify Song URI
    :return: Void
    """
    sp.add_to_queue(uri)

def spotify_artists(artist_id):
    """
    Gets the names of artists from a list of the artist’s ID, URI or URL
    :param artist_id: List of artist ID, URI, or URLs
    :return: A list of strings representing the names of the artists
    """
    sp.artists(artist_id)

def spotify_current_playback():
    """
    Get information about user’s current playback
    :return:???
    """
    sp.current_playback()




#results = sp.current_user_saved_tracks()
#for idx, item in enumerate(results['items']):
#    track = item['track']
#    print(idx, track['artists'][0]['name'], " – ", track['name'])