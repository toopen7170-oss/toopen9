from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

# 화면 배경 및 기본 설정
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class MainScreen(Screen):
    """ 전체 검색 및 계정 목록 화면 """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 전체 검색바
        search_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        self.search_input = TextInput(hint_text='계정, 캐릭터, 장비 등 검색...', multiline=False)
        search_btn = Button(text='검색', size_hint_x=0.2, background_color=(0, 0.5, 1, 1))
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # 계정 목록 영역
        scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        scroll.add_widget(self.acc_list)
        layout.add_widget(scroll)
        
        # 하단 계정 추가 버튼
        add_acc_btn = Button(text='계정 추가 (+)', size_hint_y=0.1, background_color=(0, 0.7, 0, 1))
        layout.add_widget(add_acc_btn)
        
        self.add_widget(layout)

class CharSelectScreen(Screen):
    """ 계정 클릭 시 나타나는 6개 캐릭터 창 """
    pass

class DetailScreen(Screen):
    """ 캐릭터 세부 정보 및 인벤토리 """
    pass

class PT1Manager(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    PT1Manager().run()
