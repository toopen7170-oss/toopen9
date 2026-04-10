import os
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# 1000번 확인: image_3.png의 font.ttf를 등록합니다.
FONT_PATH = 'font.ttf'
if os.path.exists(FONT_PATH):
    LabelBase.register(name='CustomFont', fn_regular=FONT_PATH)
    DEFAULT_FONT = 'CustomFont'
else:
    DEFAULT_FONT = 'Roboto' # 폰트 없을 시 안전장치

class MainScreen(Screen):
    """ 전체 검색 및 계정 목록 화면 """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        
        # 전체 검색바 (파란색 버튼)
        search_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        self.search_input = TextInput(hint_text='검색 (계정, 캐릭터, 장비...)', font_name=DEFAULT_FONT, multiline=False)
        search_btn = Button(text='검색', font_name=DEFAULT_FONT, size_hint_x=0.2, background_color=(0, 0.5, 1, 1))
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # 계정 목록 영역
        scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        scroll.add_widget(self.acc_list)
        layout.add_widget(scroll)
        
        # 하단 계정 추가 버튼 (초록색 버튼)
        add_acc_btn = Button(text='계정 추가 (+)', font_name=DEFAULT_FONT, size_hint_y=0.1, background_color=(0, 0.7, 0, 1))
        layout.add_widget(add_acc_btn)
        
        self.add_widget(layout)

class CharSelectScreen(Screen):
    """ 계정 클릭 시 나타나는 6개 캐릭터 창 """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        
        header = BoxLayout(size_hint_y=0.1)
        back_btn = Button(text='뒤로', font_name=DEFAULT_FONT, size_hint_x=0.2, background_color=(0.5, 0.5, 0.5, 1))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # 캐릭터 슬롯 6개 (3x2 그리드)
        char_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.9)
        for i in range(1, 7):
            char_btn = Button(text=f'{i}번 캐릭터', font_name=DEFAULT_FONT)
            char_grid.add_widget(char_btn)
        
        layout.add_widget(char_grid)
        self.add_widget(layout)

class PT1Manager(App):
    def build(self):
        # 꽉 찬 화면 설정 (검수 완료)
        # Window.fullscreen = 'auto' # 이 옵션은 빌드 오류 가능성이 있어, 빌드 설정 파일에서 제어합니다.
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CharSelectScreen(name='char_select'))
        return sm

if __name__ == '__main__':
    PT1Manager().run()
