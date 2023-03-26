import openai
import API_KEY
import queue
import spotipy as sp

# Set up the OpenAI API client
openai.api_key = API_KEY.api_key

# Set up the model and prompt
model_engine = "text-davinci-003"


class PromptResponder:
    def __init__(self, prompt: str, print_io=0):
        self.prompt = prompt
        self.average_call = 0
        self.number_of_calls = 0
        self.print_io = print_io

    def get_response(self, user_input: str):
        input_prompt = "Context: \"" + self.prompt + "\"\n\nUser input: \"" + user_input + "\"\n"
        if self.print_io:
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


class VoiceAssistant:
    def __init__(self, print_io=0):
        self.print_io = print_io
        self.prompt_responder = PromptResponder("""
        The user can ask two types of questions, and you will respond with an answer if enough information is given.
        - If there is not enough information to answer the question with certainty, ask a follow up question.
        The first type of question will use information you know from the internet.
        - Attempt to answer like this unless the user requests information that is not available on the internet.
        - These will likely be a majority of the questions.
        The second type of question will use of a set of given functions to answer the question by writing a python script.
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
        User input: "Skip two songs.", output: "Python Script: sp.next_track(), sp.next_track()"
        A complex example for the second type of question when it is possible is;
        User input: "Create a new playlist called party time, and add 10 taylor swift songs.", output: "Python Script: sp.user_playlist_add_tracks(sp.current_user()['uri'], sp.user_playlist_create(sp.current_user()['display_name'], 'Party Time', public='True', collaborative='False', description='')['id'], [sub['id'] for sub in sp.search('artist:Taylor Swift', limit=10, type='track')['tracks']['items']])"
        An example for the second type of question when it is not possible is;
        User input: "How many computers do I own?", output: "Python Script: Not available"
        An example for either when not enough information is given:
        User input: "Skip 2", output: "What do you mean by skip 2?"
        """)

    def get_response(self, user_input, response_queue):
        prompt_output = self.prompt_responder.get_response(user_input)
        execute_flag = 0

        if "Python Script: " in prompt_output:
            execute_flag = 1
            GPT_output = prompt_output[prompt_output.find('Python Script: ') + 15:]
            if GPT_output[-1] == "\"":
                GPT_output = GPT_output[0:-1]
            if self.print_io:
                print(GPT_output)
            # prompt_output = exec(prompt_output)
        else:
            GPT_output = prompt_output[prompt_output.find('Answer: ') + 8:]
            if GPT_output[-1] == "\"":
                GPT_output = GPT_output[0:-1]
            if GPT_output[0] == "\"":
                GPT_output = GPT_output[1:]
            if self.print_io:
                print(GPT_output)

        response_queue.put([GPT_output, execute_flag])
        return [GPT_output, execute_flag]

# print(prompt_responder.get_response("Hey, can you skip the next two songs?"))
# print(prompt_responder.get_response("Generate me a new spotify playlist with some random songs in it."))
# print(prompt_responder.get_response("Generate me a new spotify playlist called test with some random songs in it."))
# print(prompt_responder.get_response("How many playlists do I have?"))
# print(prompt_responder.get_response("How many liked songs do I have?"))
