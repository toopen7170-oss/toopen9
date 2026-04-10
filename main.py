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
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock

# --- [1단계: 폰트 및 설정] ---
FONT_FILE = "font.ttf"
DF = None # Default Font

#: 폰트가 깨지지 않도록 등록합니다.
try:
    if os.path.exists(FONT_FILE):
        LabelBase.register(name="KFont", fn_regular=FONT_FILE)
        DF = "KFont"
        Config.set('kivy', 'default_font', ['KFont', FONT_FILE, FONT_FILE, FONT_FILE, FONT_FILE])
except: pass

# 🛠️ [핵심 수정 1:]: 키보드가 올라올 때 입력을 가리지 않도록 설정합니다.
Window.softinput_mode = "below_target"

# 데이터 저장소
store = JsonStore('priston_tale_data.json')

class SInput(TextInput):
    """ 커스텀 입력창: 폰트 자동 적용 및 크기 최적화 """
    def __init__(self, **kw):
        super().__init__(**kw)
        if DF: self.font_name = DF
        self.size_hint_y = None
        self.height = 110 #의 팝업 크기에 맞춰 최적화

class SBtn(Button):
    """ 커스텀 버튼: 폰트 자동 적용 및 크기 최적화 """
    def __init__(self, **kw):
        super().__init__(**kw)
        if DF: self.font_name = DF
        self.size_hint_y = None
        self.height = 140

# --- [2단계: 화면 구성] ---
class MainMenu(Screen):
    def on_enter(self): self.refresh()
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 제목
        lbl = Label(text="[PT1 통합 검색]", font_size='22sp', size_hint_y=0.1)
        if DF: lbl.font_name = DF
        layout.add_widget(lbl)
        
        # 검색바
        s_box = BoxLayout(size_hint_y=None, height=120, spacing=5)
        self.stti = SInput(hint_text="계정, 캐릭터, 장비 검색...", multiline=False)
        s_btn = Button(text="검색", size_hint_x=0.25, background_color=(0.2, 0.6, 1, 1))
        if DF: s_btn.font_name = DF
        s_btn.bind(on_release=self.refresh)
        s_box.add_widget(self.stti); s_box.add_widget(s_btn); layout.add_widget(s_box)

        # 새 계정 만들기 버튼
        add_btn = SBtn(text="+ 새 계정 만들기", background_color=(0.1, 0.7, 0.3, 1))
        add_btn.bind(on_release=self.add_pop)
        layout.add_widget(add_btn)

        # 계정 목록 (스크롤)
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll = ScrollView(); scroll.add_widget(self.grid); layout.add_widget(scroll)
        
        self.add_widget(layout)

    def refresh(self, *a):
        """ 목록 갱신 및 계정 이동 기능 복구 """
        self.grid.clear_widgets()
        q = self.stti.text.strip().lower()
        for k in list(store.keys()):
            if not q or q in k.lower():
                row = BoxLayout(size_hint_y=None, height=140, spacing=5)
                # 🛠️ [핵심 수정 2:]: 버튼 클릭 시 'go_acc' 함수를 호출하도록 수정합니다.
                acc_btn = SBtn(text=f"계정: {k}", size_hint_x=0.8, background_color=(0.1, 0.2, 0.4, 1))
                acc_btn.bind(on_release=lambda x, name=k: self.go_acc(name))
                
                del_btn = Button(text="X", size_hint_x=0.2, background_color=(0.8, 0.2, 0.2, 1))
                if DF: del_btn.font_name = DF
                row.add_widget(acc_btn); row.add_widget(del_btn); self.grid.add_widget(row)

    def go_acc(self, name):
        """: 캐릭터 선택 화면으로 이동합니다. """
        self.manager.current_acc = name
        self.manager.current = 'char_select'

    def add_pop(self, *a):
        """: 계정 추가 팝업의 폰트와 크기를 수정합니다. """
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # 🛠️ [핵심 수정 3:]: 팝업의 라벨에도 폰트를 적용합니다.
        title_lbl = Label(text="새 계정 추가", size_hint_y=0.2, font_size='18sp')
        if DF: title_lbl.font_name = DF
        content.add_widget(title_lbl)
        
        self.acc_input = SInput(hint_text="계정 이름 입력")
        content.add_widget(self.acc_input)
        
        btn = SBtn(text="생성", background_color=(0.1, 0.7, 0.3, 1))
        content.add_widget(btn)
        
        # 🛠️ [핵심 수정 4:]: 팝업 크기를 최적화하여 키보드 가림을 방지합니다.
        self.pop = Popup(title="", content=content, size_hint=(0.85, 0.5), separator_height=0)
        btn.bind(on_release=self.create_acc)
        self.pop.open()

    def create_acc(self, *a):
        name = self.acc_input.text.strip()
        if name and not store.exists(name):
            store.put(name, chars={str(i): {"이름": f"슬롯 {i}"} for i in range(1, 7)})
            self.pop.dismiss()
            self.refresh()

class CharSelect(Screen):
    """ 캐릭터 선택 화면 (계정 클릭 시 이동) """
    def on_enter(self):
        self.clear_widgets()
        acc = self.manager.current_acc
        layout = BoxLayout(orientation='vertical', padding=10)
        lbl = Label(text=f"[{acc}] 캐릭터 선택", size_hint_y=0.1, font_size='20sp')
        if DF: lbl.font_name = DF
        layout.add_widget(lbl)
        # (여기에 6개 캐릭터 슬롯 구현 예정)
        back_btn = SBtn(text="뒤로가기")
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class PristonApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.current_acc = ""
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharSelect(name='char_select'))
        return sm

if __name__ == '__main__':
    PristonApp().run()
