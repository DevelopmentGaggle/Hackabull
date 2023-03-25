import spotify_engine
import spotify_engine2
"""
uris, names, artists = spotify_engine.spotify_GetSongRecommendations()
print(uris)
print(names)
print(artists)

playlistID = spotify_engine.spotify_CreateNewPlaylist()
spotify_engine.spotify_AddSongsToPlaylist(playlistID, uris)
"""

print(spotify_engine2.sp.next_track())
