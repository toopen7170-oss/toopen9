from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
import os

# 폰트 로딩 시 무조건 에러를 막는 예외 처리
def get_font():
    return "font.ttf" if os.path.exists("font.ttf") else None

class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=20)
        lbl = Label(text="PT1 Manager 정상 실행", font_name=get_font())
        btn = Button(text="인벤토리 관리 시작", font_name=get_font())
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'inv'))
        layout.add_widget(lbl); layout.add_widget(btn)
        self.add_widget(layout)

class InventoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical', padding=10)
        self.layout.add_widget(Label(text="[인벤토리]", font_name=get_font()))
        btn = Button(text="뒤로 가기", font_name=get_font())
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        self.layout.add_widget(btn)
        self.add_widget(self.layout)

class FinalApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(InventoryScreen(name='inv'))
        return sm

if __name__ == '__main__':
    FinalApp().run()
