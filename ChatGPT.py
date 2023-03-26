import openai
import API_KEY
import spotify_engine as sp

# Set up the OpenAI API client
openai.api_key = API_KEY.api_key

# Set up the model and prompt
model_engine = "text-davinci-003"


class PromptResponder:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.average_call = 0
        self.number_of_calls = 0

    def get_response(self, user_input: str):
        input_prompt = "Context: \"" + self.prompt + "\"\n\nUser input: \"" + user_input + "\"\n"
        print(input_prompt)
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=input_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        self.average_call = (completion.response_ms + self.average_call * self.number_of_calls) / (self.number_of_calls + 1)
        self.number_of_calls += 1

        return completion.choices[0].text


# prompt_responder = PromptResponder("""
# The user can ask two types of questions, and you will respond with an answer if enough information is given or ask additional clarifying questions until enough information has been gathered.
# The first type of question will use information you know from the internet.
# - Attempt to answer like this unless the user requests information that is not available on the internet.
# - These will likely be a majority of the questions.
# The second type of question will use of a set of given functions to answer the question.
# - This second type of question will often ask for information that you do not directly know.
# - Using the given functions, craft a python script that will answer the question.
# - DO NO USE ANY OTHER FUNCTIONS OTHER THAN THE ONES DEFINED. You must only use the functions defined below.
# - Especially if no answer is possible, consider answering the question using the first method defined above, using its formatting.
#
#
# A list of all the available functions you can use are included below.
# Function descriptions start:
# 1. sp.spotify_GetSongRecommendations(genres=\"pop\", seed_artists=\'0\', seed_tracks=\'0\', limit=5, market=\"US\", danceability=\"0.9\"):
#     This function can be used to generate a list of spotify song recommendations.
#     :param genres: A string.The genre of music that the song recommendations should fall under. The default value is \"pop\".
#     :param seed_artists: A string. A spotify artist ID. The recommended songs will be similar to this artist's music. The default value \'0\' indicates that a specific artist should not be considered when generating the recommended songs.
#     :param seed_tracks:A string. A spotify track ID. The recommended songs will be similar to this song. The default value \'0\' indicates that a specific track should not be considered when generating the recommended songs.
#     :param limit: An integer. The number of song recommendations to generate. The default value 5 will generate a list of 5 songs.
#     :param market: A string. The country that the songs are intended for. The default value of \"US\" means that the songs will be popular in the US market.
#     :param danceability: A decimal number. A measure of how danceable the song recommendations should be on a scale of 0.0 to 1.0. The default value of 0.9 is very danceable.
#     :return: A tuple of 3 values. The first value is a list of the spotify track IDs. The second value is a list of the song track names. The thrid value is a list of the corresponding artist names.
#
# 2. sp.spotify_CreateNewPlaylist(playlistName=\"My AI Generated Playlist\", public=False):
#     This function creates a new, empty spotify playlist.
#     :param playlistName: A string. This is the name of the playlist. The default value \"My AI Generated Playlist\" will create a new playlist titled \"My AI Generated Playlist\".
#     :param public: A boolean. A value of True will make the playlist publicly accessable. A value of False will make the playlist private so only the user can access it. The default value is False.
#     :return: A single value which is the spotify ID of the newly created playlist.
#
# 3. sp.spotify_AddSongsToPlaylist(playlistID, songURIs):
#     This function adds a list of songs to an existing playlist.
#     :param playlistID: A string. The spotify ID of the playlist to add songs too. This parameter is required.
#     :param songURIs: A list of strings representing the spotify IDs of the tracks.
#     :return: returns 0 to indicate the operation was successful
#
# End of function descriptions, no other functions defined.
#
# A few examples with proper formatting are provided below for how to answer the user prompts:
# An example for the first type of question is;
# input: "How old Benjamin Franklin was when he died?", output: "Answer: Benjamin Franklin was 84 years old when he died.".
# An simple example for the second type of question when it is possible is;
# input: "How many liked songs do I have on my spotify account?", output: "Python Script: sp.spotify_get_liked_count()"
# A complex example for the second type of question when it is possible is;
# input: "Generate me a new spotify playlist with some random songs in it.", output: "Python Script: sp.spotify_AddSongsToPlaylist(sp.spotify_CreateNewPlaylist(), sp.spotify_GetSongRecommendations()[0])"
# An example for the second type of question when it is not possible is;
# input: "How many computers do I own?", output: "Python Script: N/A"
# """)

prompt_responder = PromptResponder("""
The user can ask two types of questions, and you will respond with an answer if enough information is given or ask additional clarifying questions until enough information has been gathered.
The first type of question will use information you know from the internet.
- Attempt to answer like this unless the user requests information that is not available on the internet.
- These will likely be a majority of the questions.
The second type of question will use of a set of given functions to answer the question.
- This second type of question will often ask for information that you do not directly know.
- Using the given functions, craft a python script that will answer the question.
- DO NO USE ANY OTHER FUNCTIONS OTHER THAN THE ONES DEFINED. You must only use the functions defined below.
- Especially if no answer is possible, consider answering the question using the first method defined above, using its formatting.


A list of all the available functions you can use are included below.
You may use any of these functions from the spotipy API.
Do not use any other functions from the spotipy API.
Do not use any other functions not included in the spotipy API to handle this type of question.
1. sp.add_to_queue(uri, device_id=None)
2. sp.album(album_id, market=None)
3. sp.album_tracks(album_id, limit=50, offset=0, market=None)
4. sp.albums(albums, market=None)
5. sp.artist(artist_id)
6. sp.artist_albums(artist_id, album_type=None, country=None, limit=20, offset=0)
7. sp.artist_related_artists(artist_id)
8. sp.artist_top_tracks(artist_id, country='US')
9. sp.artists(artists)
10. sp.available_markets()
11. sp.current_playback(market=None, additional_types=None)
12. sp.current_user()
13. sp.current_user_follow_playlist(playlist_id)
14. sp.current_user_followed_artists(limit=20, after=None)
15. sp.current_user_following_artists(ids=None)
16. sp.current_user_following_users(ids=None)
17. sp.current_user_playing_track()
18. sp.current_user_playlists(limit=50, offset=0)
19. sp.current_user_recently_played(limit=50, after=None, before=None)
20. sp.current_user_saved_albums(limit=20, offset=0, market=None)
21. sp.current_user_saved_albums_add(albums=[])
22. sp.current_user_saved_albums_contains(albums=[])
23. sp.current_user_saved_episodes(limit=20, offset=0, market=None)
24. sp.current_user_saved_episodes_add(episodes=None)
25. sp.current_user_saved_episodes_contains(episodes=None)
26. sp.current_user_saved_shows(limit=20, offset=0, market=None)
27. sp.current_user_saved_shows_add(shows=[])
28. sp.current_user_saved_shows_contains(shows=[])
29. sp.current_user_saved_tracks(limit=20, offset=0, market=None)
30. sp.current_user_saved_tracks_add(tracks=None)
31. sp.current_user_saved_tracks_contains(tracks=None)
32. sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
33. sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')
34. sp.currently_playing(market=None, additional_types=None)
35. sp.devices()
36. sp.episode(episode_id, market=None)
37. sp.episodes(episodes, market=None)
38. sp.featured_playlists(locale=None, country=None, timestamp=None, limit=20, offset=0)
39. sp.me()
40. sp.new_releases(country=None, limit=20, offset=0)
41. sp.next(result)
42. sp.next_track(device_id=None)
43. sp.pause_playback(device_id=None)
44. sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
45. sp.playlist_add_items(playlist_id, items, position=None)
46. sp.playlist_change_details(playlist_id, name=None, public=None, collaborative=None, description=None)
47. sp.playlist_cover_image(playlist_id)
48. sp.playlist_is_following(playlist_id, user_ids)
49. sp.playlist_items(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
50. sp.playlist_reorder_items(playlist_id, range_start, insert_before, range_length=1, snapshot_id=None)
51. sp.playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', ))
52. sp.previous(result)
53. sp.previous_track(device_id=None)
54. sp.queue()
55. sp.recommendation_genre_seeds()
56. sp.recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)
57. sp.repeat(state, device_id=None)
58. sp.search(q, limit=10, offset=0, type='track', market=None)
59. sp.search_markets(q, limit=10, offset=0, type='track', markets=None, total=None)
60. sp.seek_track(position_ms, device_id=None)
61. sp.show(show_id, market=None)
62. sp.show_episodes(show_id, limit=50, offset=0, market=None)
63. sp.shows(shows, market=None)
64. sp.shuffle(state, device_id=None)
65. sp.start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)
66. sp.track(track_id, market=None)
67. sp.tracks(tracks, market=None)
68. sp.transfer_playback(device_id, force_play=True)
69. sp.user(user)
70. sp.user_follow_artists(ids=[])
71. sp.user_follow_users(ids=[])
72. sp.user_playlist(user, playlist_id=None, fields=None, market=None)
73. sp.user_playlist_add_episodes(user, playlist_id, episodes, position=None)
74. sp.user_playlist_add_tracks(user, playlist_id, tracks, position=None)
75. sp.user_playlist_change_details(user, playlist_id, name=None, public=None, collaborative=None, description=None)
76. sp.user_playlist_create(user, name, public=True, collaborative=False, description='')
77. sp.user_playlist_follow_playlist(playlist_owner_id, playlist_id)
78. sp.user_playlist_is_following(playlist_owner_id, playlist_id, user_ids)
79. sp.user_playlist_reorder_tracks(user, playlist_id, range_start, insert_before, range_length=1, snapshot_id=None)
80. sp.user_playlists(user, limit=50, offset=0)
81. sp.volume(volume_percent, device_id=None)
End of the available spotify functions.
 
End of function descriptions, no other functions defined.

A few examples with proper formatting are provided below for how to answer the user prompts:
An example for the first type of question is;
User input: "How old Benjamin Franklin was when he died?", output: "Answer: Benjamin Franklin was 84 years old when he died."
An simple example for the second type of question when it is possible is;
User input: "Skip the next song.", output: "Python Script: sp.next_track()"
A complex example for the second type of question when it is possible is;
User input: "Generate me a new spotify playlist with some random songs in it.", output: "Python Script: sp.spotify_AddSongsToPlaylist(sp.spotify_CreateNewPlaylist(), sp.spotify_GetSongRecommendations()[0])"
An example for the second type of question when it is not possible is;
User input: "How many computers do I own?", output: "Python Script: N/A"
""")

prompt_output = prompt_responder.get_response("What time is it?")
print(prompt_output)

# if "Python Script: " in prompt_output:
#     print(1)
#     # TODO May not work!!! Will work mostly though
#     # prompt_output = prompt_output.replace("Output: \"Python Script: ", "")
#     # prompt_output = prompt_output[0:-1]
#     # It is not working because it will change if it is outputing output or answer on occasion.
#     prompt_output = exec(prompt_output)
#     print(prompt_output)
# else:
#     print(2)
#     print(prompt_output)


# print(prompt_responder.get_response("Generate me a new spotify playlist with some random songs in it."))
# print(prompt_responder.get_response("Generate me a new spotify playlist called test with some random songs in it."))
# print(prompt_responder.get_response("How many playlists do I have?"))
# print(prompt_responder.get_response("How many liked songs do I have?"))


# prompt_responder = PromptResponder("""
# Given the following user prompt, answer it by crafting a python script.
#
# """)
#
# print(prompt_responder.get_response("Using the Spotipy library, get the most recent liked song."))