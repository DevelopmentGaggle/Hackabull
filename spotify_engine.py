import requests
import json

# Configuration
token = \
    "BQAYALG5LlC3N0_qTYq_SXWTC61gM0OPXJWi6MyBiufwKcYWA-IIGRezsbVh5kSe6yGh53RvBpWs2YiV7Zpj0Q8T25CepMmScFdxx_58ALlKe1XGrTCNAcrICXVi49QpKDMd76OvTmJA5hVODPlXGqLfMMbgaPCFhaf53w9_E-G2DWmLsq4Jw1rjPdMyLF81sYoOPWgeUhxSqY60GwJUD2ML7WZCA41OtbGl79irAFmlwcsNQgPyAXe_P5W_QqyPIcMVF_-0rvv9uWHd4HZWCw_ygxvwMO8I0hbyM6-7AyI41arcNVR5MF8NIq2lTdXbUI_Oy4gcMtvb_g"
user_id = "rvwo6t4opi64jp86slw1qkihh"

def spotify_GetSongRecommendations(genres="jazz", seed_artists='0', seed_tracks='0', limit=5, market="US", danceability="0.9"):
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
    # FILL THE NEW PLAYLIST WITH THE RECOMMENDATIONS
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks"

    request_body = json.dumps({
              "uris" : songURIs
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json",
                            "Authorization":f"Bearer {token}"})

    print(response.status_code)

    return 0
