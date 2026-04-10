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
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.config import Config

# --- [폰트 및 설정] ---
FONT_NAME = "KFont"
FONT_FILE = "font.ttf"
if os.path.exists(FONT_FILE):
    LabelBase.register(name=FONT_NAME, fn_regular=FONT_FILE)
    Config.set('kivy', 'default_font', [FONT_NAME, FONT_FILE])
else:
    FONT_NAME = None

# 데이터 저장소
store = JsonStore('priston_tale_data.json')

class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        if FONT_NAME: self.font_name = FONT_NAME
        self.size_hint_y = None
        self.height = 130 # 버튼 크기 통일

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        if FONT_NAME: self.font_name = FONT_NAME

class SInput(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        if FONT_NAME: self.font_name = FONT_NAME
        self.size_hint_y = None
        self.height = 110 # 검색창 크기 통일

# --- [화면 구성: 핵심 수정] ---
class MainMenu(Screen):
    def on_enter(self): self.refresh()
    def __init__(self, **kw):
        super().__init__(**kw)
        # 전체 레이아웃 (세로 방향)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 제목
        lbl = SLabel(text="[PT1 통합 검색]", font_size='22sp', size_hint_y=0.1)
        self.layout.add_widget(lbl)
        
        #
        s_box = BoxLayout(size_hint_y=None, height=120, spacing=5)
        self.stti = SInput(hint_text="계정, 캐릭터, 장비 검색...", multiline=False)
        s_btn = Button(text="검색", size_hint_x=0.25, background_color=(0.2, 0.6, 1, 1))
        if FONT_NAME: s_btn.font_name = FONT_NAME
        s_btn.bind(on_release=self.refresh)
        s_box.add_widget(self.stti); s_box.add_widget(s_btn); self.layout.add_widget(s_box)

        # 🛠️: 새 계정 만들기 버튼을 검색창 바로 아래로 배치합니다.
        add_btn = SBtn(text="+ 새 계정 만들기", background_color=(0.1, 0.7, 0.3, 1))
        
        # 🛠️: 버튼 클릭 시 계정 추가 팝업이 뜨도록 코드를 'bind'(연결)합니다.
        add_btn.bind(on_release=self.add_pop)
        self.layout.add_widget(add_btn)

        # 계정 목록 (스크롤 가능)
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll = ScrollView(); scroll.add_widget(self.grid); self.layout.add_widget(scroll)
        
        self.add_widget(self.layout)

    def refresh(self, *a):
        self.grid.clear_widgets()
        q = self.stti.text.strip().lower()
        for k in list(store.keys()):
            if not q or q in k.lower():
                row = BoxLayout(size_hint_y=None, height=140, spacing=5)
                acc_btn = SBtn(text=f"계정: {k}", size_hint_x=0.8, background_color=(0.1, 0.2, 0.4, 1))
                del_btn = Button(text="X", size_hint_x=0.2, background_color=(0.8, 0.2, 0.2, 1))
                if FONT_NAME: del_btn.font_name = FONT_NAME
                row.add_widget(acc_btn); row.add_widget(del_btn); self.grid.add_widget(row)

    # 🛠️ 계정 추가 팝업 기능 (사용자님 요청 작동 확인 완료)
    def add_pop(self, *a):
        c = BoxLayout(orientation='vertical', padding=10, spacing=10)
        inp = SInput(hint_text="계정 이름 입력")
        btn = SBtn(text="생성", background_color=(0.1, 0.7, 0.3, 1))
        c.add_widget(inp); c.add_widget(btn)
        pop = Popup(title="계정 추가", content=c, size_hint=(0.8, 0.4))
        def save(x):
            if inp.text.strip():
                store.put(inp.text.strip(), chars={str(i): {"이름": f"슬롯 {i}"} for i in range(1, 7)})
                pop.dismiss(); self.refresh()
        btn.bind(on_release=save); pop.open()

class PristonApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main'))
        return sm

if __name__ == '__main__':
    PristonApp().run()
