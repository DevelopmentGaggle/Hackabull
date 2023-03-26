from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import datadog
from kivy.clock import Clock
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivy.config import Config
import time


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


class ChatWindow(Screen):
    pass


class OprWindow(Screen):
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
        self.theme_cls.accent_palette = "Gray"

        kv = Builder.load_file('app.kv')
        return kv

    def on_load(self):
        self.root.current = 'chat'
        # If the screen is empty, add a prompt to the chat list
        if len(self.root.ids.main_screen.ids.chatlist.children) == 0:
            self.add_message("Voice Assistant", "Hello, ask me a question!")

        # Load TTS thread
        self.data_doggo.run_stt()

        # Function to execute every cycle
        Clock.schedule_interval(self.periodic, 1 / 30.)

    def periodic(self, french_roast):
        if not self.data_doggo.stt_to_GUI.empty():
            response = self.data_doggo.stt_to_GUI.get()

            # If the data is fresh, make a new prompt
            if self.fresh_data:
                self.add_message("User", response[0])
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

    def add_message(self, name, text):
        CGPT = "Assistant"
        if name == CGPT:
            icon = 'robot-happy-outline'
            radius = [50, 50, 50, 0]
            color = self.theme_cls.primary_dark
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

    # Functions to modify the spotify specific things, but could theoretically be used in other cases
    def api_name(self):
        pass

    # Will be used for album covers
    def change_picture(self):
        pass

    # Will be used for song names
    def primary_text(self):
        pass

    # Will be used for artist names
    def secondary_text(self):
        pass


PromptifyApp().run()


