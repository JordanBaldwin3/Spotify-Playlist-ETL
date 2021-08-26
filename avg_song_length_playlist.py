import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import boto3
from datetime import datetime

from config.playlists import spotify_playlist
from tools.playlists import get_tracks_from_playlist


auth_manager = SpotifyClientCredentials(client_id='4d999c3ef22443baa461d1925045f700',
        client_secret='')
spotipy_object = spotipy.Spotify(auth_manager=auth_manager)


PLAYLIST = 'steppin_out'

# Writes a CSV file using the data dictionary contents as headers
# uses a previous function to get all the tracks from a given playlist
# For each track, it gets the duration, track name, all of the feature
#  artists and calculates the total number of artists on a track.
# It then writes all of this info to a csv file while also returning a data dict
def gather_data_local():

    data_dict = {
    'Song Length': [],
    'Song Name': [],
    'Artists': [],
    'Artist Count': []

    }

    with open("steppin_out_songs.csv", 'w') as file:
        header = list(data_dict.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        songs_obtained = []

        tracks = get_tracks_from_playlist(spotify_playlist()[PLAYLIST])
 
        for track in list(tracks.keys()):
            track_info = spotipy_object.track(track)
            track_duration = track_info['duration_ms']

            artist_combined = []
            for i in range(len(track_info['artists'])):
                artist_count = i + 1
                artist_combined.append(track_info['artists'][i]['name'])

            writer.writerow({'Song Length': track_duration,
                             'Song Name': track_info['name'],
                             'Artists': artist_combined,
                             'Artist Count': artist_count})

            data_dict['Song Length'].append(track_duration)
            data_dict['Song Name'].append(track_info['name'])
            data_dict['Artists'].append(artist_combined)
            data_dict['Artist Count'].append(artist_count)

    return data_dict

# Same as previous function except this loads the csv to s3 bucket
# This returns an s3 response to upload to the datalake
def gather_data():

    with open("steppin_out_songs.csv", 'w') as file:
        header = ['Song Length', 'Song Name', 'Artists', 'Artist Count']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        songs_obtained = []

        tracks = get_tracks_from_playlist(spotify_playlist()[PLAYLIST])

        for track in list(tracks.keys()):

            track_info = spotipy_object.track(track)
            track_duration = track_info['duration_ms']

            artist_combined = []
            for i in range(len(track_info['artists'])):
                artist_count = i + 1
                artist_combined.append(track_info['artists'][i]['name'])

            writer.writerow({'Song Length': track_duration,
                             'Song Name': track_info['name'],
                             'Artists': artist_combined,
                             'Artist Count': artist_count})

    s3_resource = boto3.resource('s3',
         aws_access_key_id='',
         aws_secret_access_key='')
    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/steppin_out_songs.csv'
    response = s3_resource.Object('spotify-api-analysis-data', filename).upload_file("steppin_out_songs.csv")

    return response

def lambda_handler(event, context):
    gather_data()

if __name__ == '__main__':
    data = gather_data_local()