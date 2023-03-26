from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import datadog
from kivy.clock import Clock
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget


#Define windows
class LogInScreen(Screen):
    pass

class ChatWindow(Screen):
    pass

class OprWindow(Screen):
    pass

#Screen manager
class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):

    data = {
        'Python': 'language-python',
        'PHP': 'language-php',
        'C++': 'language-cpp',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_doggo = datadog.DataDog()


    def build(self):
#colors
        '''Red', 'Pink', 'Purple', 'DeepPurple', '
        Indigo', 'Blue', 'LightBlue', 'Cyan',
        'Teal', 'Green', 'LightGreen', 'Lime',
        'Yellow', 'Amber', 'Orange', 'DeepOrange',
        'Brown', 'Gray', 'BlueGray'''
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Red"
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
            if response[1]:
                self.add_message("User", response[0])
            else:
                self.edit_message(response[0])

    def add_message(self, name, text):
        CGPT = "Tesss"
        if name == CGPT:
            icon = 'robot-happy-outline'
            radius = [50, 50, 50, 0]
            color = self.theme_cls.primary_dark
        else:
            icon = 'account-circle-outline'
            radius = [50, 50, 0, 50]
            color = self.theme_cls.primary_color
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

    def edit_message(self, text):
        self.root.ids.main_screen.ids.chatlist.children[0].secondary_text = text


MainApp().run()

