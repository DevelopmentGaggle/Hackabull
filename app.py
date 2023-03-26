from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import datadog
from kivy.clock import Clock
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivy.config import Config
import time
import spotipy as sp


# https://github.com/kivy/kivy/pull/7299
# Helps with screen blurriness on Windows
from ctypes import windll, c_int64
from kivy.core.window import Window
windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
Window.maximize()
Config.set('kivy', 'exit_on_escape', '0')


# Define windows
class LogInScreen(Screen):
    pass

class SignInScreen(Screen):
    pass


class ChatWindow(Screen):
    pass


class OprWindow(Screen):
    pass

class AccountWindow(Screen):
    pass

class HistoryWindow(Screen):
    pass


# Screen manager
class WindowManager(ScreenManager):
    pass


class PromptifyApp(MDApp):

    data = {
        'Python': 'language-python',
        'PHP': 'language-php',
        'C++': 'language-cpp',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_doggo = datadog.DataDog()
        self.fresh_data = True
        self.last_song = ""
        self.user_name = "user"
        self.mute = False

    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        # colors
        '''Red', 'Pink', 'Purple', 'DeepPurple', '
        Indigo', 'Blue', 'LightBlue', 'Cyan',
        'Teal', 'Green', 'LightGreen', 'Lime',
        'Yellow', 'Amber', 'Orange', 'DeepOrange',
        'Brown', 'Gray', 'BlueGray'''
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"

        kv = Builder.load_file('app.kv')
        return kv

    def account_creation(self, name, email, password, confirm_password):
        if name == "" or email == "" or password == "":
            return

        if password != confirm_password:
            return

        self.on_load(name, password)

    def on_load(self, name, password):
        if name == "" or password == "":
            return

        name = name.capitalize()
        self.root.ids.account_screen.ids.name.text = name

        self.root.current = 'chat'
        # If the screen is empty, add a prompt to the chat list
        if len(self.root.ids.main_screen.ids.chatlist.children) == 0:
            self.add_message("Assistant", f"Hello, {name} ask me a question!")

        # Add the name of the user to a locally stored variable
        self.user_name = name

        # Load TTS thread
        self.data_doggo.run_stt()

        # Function to execute every cycle
        Clock.schedule_interval(self.periodic, 1 / 30.)

    def periodic(self, french_roast):
        if not self.data_doggo.stt_to_GUI.empty():
            response = self.data_doggo.stt_to_GUI.get()

            # If the data is fresh, make a new prompt
            if self.fresh_data:
                self.add_message(self.user_name, response[0])
                self.fresh_data = False
            else:
                if response[1]:
                    self.edit_message(response[0])
                    self.fresh_data = True
                else:
                    self.edit_message(response[0])

        if not self.data_doggo.chatGPT_to_GUI.empty():
            gpt_response = self.data_doggo.chatGPT_to_GUI.get()
            self.add_message("Assistant", gpt_response)
            self.fresh_data = True

        # If a song starts playing, switch screens
        use_last_played = 0
        song_to_display = sp.currently_playing()
        if song_to_display is None:
            use_last_played = 1
            song_to_display = sp.current_user_recently_played(limit=1)
        if song_to_display is None:
            use_last_played = 2

        # Get song name
        song_name = None
        if use_last_played == 0:
            song_name = sp.currently_playing()['item']['name']
        elif use_last_played == 1:
            song_name = sp.current_user_recently_played(limit=1)['items'][0]['track']['name']
        else:
            song_name = ""

        if song_name not in self.last_song:
            self.last_song = song_name
            self.on_transition()

    def add_message(self, name, text):
        CGPT = "Assistant"
        if name == CGPT:
            icon = 'robot-happy-outline'
            radius = [50, 50, 50, 0]
            color = self.theme_cls.primary_dark
            # if it is a gpt prompt, output it to the history
            widget_h = TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon=icon
                ),
                text=name,
                secondary_text=text,
                bg_color=color,
                radius=radius
            )
            self.root.ids.history_screen.ids.chatlist_h.add_widget(widget_h)
        else:
            icon = 'account-circle-outline'
            radius = [50, 50, 0, 50]
            # color = self.theme_cls.primary_color
            color = (30/255, 215/255, 96/255, 0.8)
        widget = TwoLineAvatarIconListItem(
            IconLeftWidget(
                icon=icon
            ),
            text=name,
            secondary_text=text,
            bg_color=color,
            radius=radius
        )
        self.root.ids.main_screen.ids.chatlist.add_widget(widget)
        widget_m = TwoLineAvatarIconListItem(
            IconLeftWidget(
                icon=icon
            ),
            text=name,
            secondary_text=text,
            bg_color=color,
            radius=radius
        )
        self.root.ids.operation_screen.ids.chatlist_m.add_widget(widget_m)

    def edit_message(self, text):
        self.root.ids.main_screen.ids.chatlist.children[0].secondary_text = text
        self.root.ids.operation_screen.ids.chatlist_m.children[0].secondary_text = text

    # Updates the screen so the two look the same
    def on_transition(self):
        if self.root.current == 'chat':
            # Update the screen before we move to it
            self.api_name("Spotify")
            use_last_played = 0

            song_to_display = sp.currently_playing()
            if song_to_display is None:
                use_last_played = 1
                song_to_display = sp.current_user_recently_played(limit=1)
            if song_to_display is None:
                use_last_played = 2

            # Will be used for album covers
            album_cover = None
            if use_last_played == 0:
                album_cover = sp.currently_playing()['item']['name']
            elif use_last_played == 1:
                album_cover = sp.current_user_recently_played(limit=1)['items'][0]['track']['name']
            else:
                album_cover = 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80'
            self.change_picture(album_cover)

            # Will be used for song names
            song_name = None
            if use_last_played == 0:
                song_name = sp.currently_playing()['item']['name']
            elif use_last_played == 1:
                song_name = sp.current_user_recently_played(limit=1)['items'][0]['track']['name']
            else:
                song_name = "Not Playing"
            self.primary_text(song_name)

            # Will be used for artist names
            artist_name = None
            if use_last_played == 0:
                artist_name = sp.currently_playing()['item']['artists'][0]['name']
            elif use_last_played == 1:
                artist_name = sp.current_user_recently_played(limit=1)['items'][0]['track']['artists'][0]['name']
            else:
                artist_name = "No Artist"
            self.secondary_text(artist_name)

            # Move to the screen
            self.get_running_app().screen_direction = "left"
            self.root.current = 'operation'

        else:
            self.get_running_app().screen_direction = "right"
            self.root.current = 'chat'

    def on_request_close(self, *args):
        print("test")
        self.data_doggo.kill_threads = True
        # time.sleep(1)
        self.stop = True

    def move_account(self, widget):
        self.root.current = 'account'

    def move_history(self):
        self.root.current = 'history'

    # Functions to modify the spotify specific things, but could theoretically be used in other cases
    def api_name(self, text):
        self.root.ids.operation_screen.ids.api_name.text = text

    # Will be used for album covers
    def change_picture(self, picture_url):
        self.root.ids.operation_screen.ids.related_image.source = picture_url

    # Will be used for song names
    def primary_text(self, text):
        self.root.ids.operation_screen.ids.primary_description.text = text

    # Will be used for artist names
    def secondary_text(self, text):
        self.root.ids.operation_screen.ids.secondary_description.text = text

    # Toggles mute condition
    def mute_microphone(self):
        self.mute = not self.mute
        if self.mute:
            self.root.ids.main_screen.ids.microphone1.icon = "microphone-off"
            self.root.ids.operation_screen.ids.microphone2.icon = "microphone-off"

        else:
            self.root.ids.main_screen.ids.microphone1.icon = "microphone"
            self.root.ids.operation_screen.ids.microphone2.icon = "microphone"

    def confirm(self):
        pass


PromptifyApp().run()


