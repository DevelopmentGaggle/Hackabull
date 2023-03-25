import spotify_engine

uris, names, artists = spotify_engine.spotify_GetSongRecommendations()
print(uris)
print(names)
print(artists)

playlistID = spotify_engine.spotify_CreateNewPlaylist()
spotify_engine.spotify_AddSongsToPlaylist(playlistID, uris)