from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import datadog
from kivy.clock import Clock

#Define windows
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
        self.datadog = datadog.DataDog


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
        # If the screen is empty, add a prompt to the chat list
        if len(self.root.ids.main_screen.ids.chatlist.children) == 0:
            self.add_message("Voice Assistant", "Hello, ask me a question!")

        # Load TTS thread
        self.datadog.run_tts()

        # Function to execute every cycle
        Clock.schedule_interval(self.periodic, 1 / 30.)

    def periodic(self):
        if not self.datadog.response.empty():
            response = self.datadog.response.get()
            if not self.datadog.is_talking:
                is_talking = True
                self.add_message("test", response[0])
            else:
                self.edit_message(response[0])

    def add_message(self, name, text):
        pass

    def edit_message(self, text):
        pass

MainApp().run()

