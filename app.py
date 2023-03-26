from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


#Define windows
class ChatWindow(Screen):
    pass

class OprWindow(Screen):
    pass

#Screen manager
class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):

    def build(self):
        # jdgskgj
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


MainApp().run()

