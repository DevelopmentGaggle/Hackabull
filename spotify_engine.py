import requests
import json

# Configuration
token = \
    "BQAYALG5LlC3N0_qTYq_SXWTC61gM0OPXJWi6MyBiufwKcYWA-IIGRezsbVh5kSe6yGh53RvBpWs2YiV7Zpj0Q8T25CepMmScFdxx_58ALlKe1XGrTCNAcrICXVi49QpKDMd76OvTmJA5hVODPlXGqLfMMbgaPCFhaf53w9_E-G2DWmLsq4Jw1rjPdMyLF81sYoOPWgeUhxSqY60GwJUD2ML7WZCA41OtbGl79irAFmlwcsNQgPyAXe_P5W_QqyPIcMVF_-0rvv9uWHd4HZWCw_ygxvwMO8I0hbyM6-7AyI41arcNVR5MF8NIq2lTdXbUI_Oy4gcMtvb_g"
user_id = "rvwo6t4opi64jp86slw1qkihh"


def spotify_GetSongRecommendations(genres="pop", seed_artists='0', seed_tracks='0', limit=5, market="US", danceability="0.9"):
    """
    This function can be used to generate a list of spotify song recommendations.
    :param genres: A string.The genre of music that the song recommendations should fall under. The default value is "pop".
    :param seed_artists: A string. A spotify artist ID. The recommended songs will be similar to this artist's music. The default value '0' indicates that a specific artist should not be considered when generating the recommended songs.
    :param seed_tracks:A string. A spotify track ID. The recommended songs will be similar to this song. The default value '0' indicates that a specific track should not be considered when generating the recommended songs.
    :param limit: An integer. The number of song recommendations to generate. The default value 5 will generate a list of 5 songs.
    :param market: A string. The country that the songs are intended for. The default value of "US" means that the songs will be popular in the US market.
    :param danceability: A decimal number. A measure of how danceable the song recommendations should be on a scale of 0.0 to 1.0. The default value of 0.9 is very danceable.
    :return: A tuple of 3 values. The first value is a list of the spotify track IDs. The second value is a list of the song track names. The thrid value is a list of the corresponding artist names.
    """
    endpoint_url = "https://api.spotify.com/v1/recommendations?"

    # FILTERS
    uris = []
    names = []
    artists = []

    # PERFORM THE QUERY
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={genres}&target_danceability={danceability}'
    if(seed_artists != '0'):
        query += f'&seed_artists={seed_artists}'
    if(seed_tracks != '0'):
        query += f'&seed_tracks={seed_tracks}'

    response = requests.get(query,
                   headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})
    json_response = response.json()
    print(json_response)
    for i, j in enumerate(json_response['tracks']):
        uris.append(j['uri'])
        names.append(j['name'])
        artists.append(j['artists'][0]['name'])

    return uris, names, artists
    #print('Recommended Songs:')
    #for i,j in enumerate(json_response['tracks']):
    #           uris.append(j['uri'])
    #          print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")

def spotify_CreateNewPlaylist(playlistName="My AI Generated Playlist", public=False):
    """
    This function creates a new, empty spotify playlist.
    :param playlistName: A string. This is the name of the playlist. The default value "My AI Generated Playlist" will create a new playlist titled "My AI Generated Playlist".
    :param public: A boolean. A value of True will make the playlist publicly accessable. A value of False will make the playlist private so only the user can access it. The default value is False.
    :return: A single value which is the spotify ID of the newly created playlist.
    """
    # CREATE A NEW PLAYLIST
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    request_body = json.dumps({
              "name": playlistName,
              "description": "This playlist was generated using AI!",
              "public": public,
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})

    url = response.json()['external_urls']['spotify']
    print(response.status_code)

    return response.json()['id']


def spotify_AddSongsToPlaylist(playlistID, songURIs):
    """
    This function adds a list of songs to an existing playlist.
    :param playlistID: A string. The spotify ID of the playlist to add songs too. This parameter is required.
    :param songURIs: A list of strings representing the spotify IDs of the tracks.
    :return: returns 0 to indicate the operation was successful
    """
    # FILL THE NEW PLAYLIST WITH THE RECOMMENDATIONS
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks"

    request_body = json.dumps({
              "uris" : songURIs
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})

    print(response.status_code)

    return 0
