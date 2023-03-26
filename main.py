import spotify_engine2
"""
uris, names, artists = spotify_engine.spotify_GetSongRecommendations()
print(uris)
print(names)
print(artists)

playlistID = spotify_engine.spotify_CreateNewPlaylist()
spotify_engine.spotify_AddSongsToPlaylist(playlistID, uris)
"""

#print(spotify_engine2.sp.current_user())
#print([sub['id'] for sub in spotify_engine2.sp.search('artist:Taylor Swift', limit=10, type='track')['tracks']['items']])
#print(spotify_engine2.sp.user_playlist_create(spotify_engine2.sp.current_user()['display_name'], 'Party Time', public='True', collaborative='False', description=''))
#sp.user_playlist_add_tracks(sp.current_user()['uri'], sp.user_playlist_create(sp.current_user()['display_name'], 'Party Time', public='True', collaborative='False', description='')['id'], [sub['id'] for sub in sp.search('artist:Taylor Swift', limit=10, type='track')['tracks']['items']])
spotify_engine2.sp.user_playlist_add_tracks(spotify_engine2.sp.current_user()['uri'], spotify_engine2.sp.user_playlist_create(spotify_engine2.sp.current_user()['display_name'], 'Party Time', public='True', collaborative='False', description='')['id'], [sub['id'] for sub in spotify_engine2.sp.search('artist:Taylor Swift', limit=10, type='track')['tracks']['items']])

#Create a new playlist called party time, and add 10 taylor swift songs