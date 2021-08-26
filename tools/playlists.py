import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(client_id='4d999c3ef22443baa461d1925045f700',
        client_secret='')
spotify = spotipy.Spotify(auth_manager=auth_manager)

# Takes in a Spotify playlist URI and returns a dictionary containing all the songs
# in that playlist, with the track URI mapped to the track name
def get_tracks_from_playlist(playlist_uri):

    tracks = {}
    playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_uri)

    for song in playlist_tracks['items']:
        if song['track']:
            tracks[song['track']['uri']] = song['track']['name']
            
    return tracks