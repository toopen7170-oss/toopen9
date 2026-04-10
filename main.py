import os
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.config import Config

# --- [폰트 설정] ---
# 폰트 파일이 저장소에 font.ttf라는 이름으로 있으므로 이를 명확히 지정합니다.
FONT_NAME = "KFont"
FONT_FILE = "font.ttf"

if os.path.exists(FONT_FILE):
    # 앱 전체에서 사용할 수 있도록 폰트를 등록합니다.
    LabelBase.register(name=FONT_NAME, fn_regular=FONT_FILE)
    # 기본 폰트를 KFont로 강제 설정하여 모든 위젯에 적용합니다.
    Config.set('kivy', 'default_font', [FONT_NAME, FONT_FILE])
else:
    FONT_NAME = None # 폰트가 없을 경우 기본값 사용

class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        if FONT_NAME: self.font_name = FONT_NAME

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        if FONT_NAME: self.font_name = FONT_NAME

class SInput(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        if FONT_NAME: self.font_name = FONT_NAME

# --- [화면 구성] ---
class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 제목 (폰트 적용)
        lbl = SLabel(text="[PT1 통합 검색]", font_size='24sp', size_hint_y=0.1)
        layout.add_widget(lbl)
        
        # 검색바
        search_layout = BoxLayout(size_hint_y=None, height=120, spacing=5)
        self.stti = SInput(hint_text="계정, 캐릭터, 장비 검색...", multiline=False)
        s_btn = SBtn(text="검색", size_hint_x=0.25, background_color=(0.2, 0.6, 1, 1))
        search_layout.add_widget(self.stti)
        search_layout.add_widget(s_btn)
        layout.add_widget(search_layout)
        
        # 계정 목록 (스크롤 가능)
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        
        # 하단 계정 생성 버튼
        add_btn = SBtn(text="+ 새 계정 만들기", background_color=(0.1, 0.7, 0.3, 1), size_hint_y=0.15)
        layout.add_widget(add_btn)
        
        self.add_widget(layout)

class PristonApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main'))
        return sm

if __name__ == '__main__':
    PristonApp().run()
