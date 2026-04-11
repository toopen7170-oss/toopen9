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

# --- [1단계: 폰트 등록 및 기본 설정] ---
FONT_FILE = "font.ttf"
DF = "KFont" if os.path.exists(FONT_FILE) else None
if DF:
    LabelBase.register(name=DF, fn_regular=FONT_FILE)
    Config.set('kivy', 'default_font', [DF, FONT_FILE, FONT_FILE, FONT_FILE])

Window.softinput_mode = "below_target"
store = JsonStore('priston_tale_data.json')

class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        if DF: self.font_name = DF
        self.size_hint_y = None
        self.height = 140

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        if DF: self.font_name = DF

# --- [2단계: 메인 메뉴 - 계정 삭제 및 검색] ---
class MainMenu(Screen):
    def on_enter(self): self.refresh()
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(SLabel(text="[PT1 통합 검색]", font_size='22sp', size_hint_y=0.1))
        
        s_box = BoxLayout(size_hint_y=None, height=120, spacing=5)
        self.stti = TextInput(hint_text="검색어 입력...", multiline=False)
        if DF: self.stti.font_name = DF
        s_btn = Button(text="검색", size_hint_x=0.25, background_color=(0.2, 0.6, 1, 1))
        if DF: s_btn.font_name = DF
        s_btn.bind(on_release=self.refresh)
        s_box.add_widget(self.stti); s_box.add_widget(s_btn); layout.add_widget(s_box)

        add_btn = SBtn(text="+ 새 계정 만들기", background_color=(0.1, 0.7, 0.3, 1))
        add_btn.bind(on_release=self.add_pop)
        layout.add_widget(add_btn)

        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll = ScrollView(); scroll.add_widget(self.grid); layout.add_widget(scroll)
        self.add_widget(layout)

    def refresh(self, *a):
        self.grid.clear_widgets()
        q = self.stti.text.strip().lower()
        for k in list(store.keys()):
            if not q or q in k.lower():
                row = BoxLayout(size_hint_y=None, height=140, spacing=5)
                acc_btn = SBtn(text=f"계정: {k}", size_hint_x=0.8, background_color=(0.1, 0.2, 0.4, 1))
                acc_btn.bind(on_release=lambda x, name=k: self.go_acc(name))
                
                # 🛠️ 삭제 확인 기능 연결
                del_btn = Button(text="X", size_hint_x=0.2, background_color=(0.8, 0.2, 0.2, 1))
                if DF: del_btn.font_name = DF
                del_btn.bind(on_release=lambda x, name=k: self.confirm_del(name))
                
                row.add_widget(acc_btn); row.add_widget(del_btn); self.grid.add_widget(row)

    # 🛠️ 멘트 팝업 추가
    def confirm_del(self, name):
        c = BoxLayout(orientation='vertical', padding=15, spacing=15)
        c.add_widget(SLabel(text=f"'{name}'\n삭제하시겠습니까?"))
        btns = BoxLayout(size_hint_y=0.4, spacing=10)
        y_btn = Button(text="삭제", background_color=(0.8, 0, 0, 1))
        n_btn = Button(text="취소")
        if DF: y_btn.font_name = DF; n_btn.font_name = DF
        btns.add_widget(y_btn); btns.add_widget(n_btn); c.add_widget(btns)
        
        pop = Popup(title="확인", content=c, size_hint=(0.8, 0.4))
        y_btn.bind(on_release=lambda x: [store.delete(name), self.refresh(), pop.dismiss()])
        n_btn.bind(on_release=pop.dismiss); pop.open()

    def go_acc(self, name):
        self.manager.current_acc = name
        self.manager.current = 'char_select'

    def add_pop(self, *a):
        c = BoxLayout(orientation='vertical', padding=10, spacing=10)
        ti = TextInput(hint_text="계정 이름", multiline=False)
        if DF: ti.font_name = DF
        b = SBtn(text="생성", background_color=(0.1, 0.7, 0.3, 1))
        c.add_widget(ti); c.add_widget(b)
        p = Popup(title="추가", content=c, size_hint=(0.8, 0.4))
        b.bind(on_release=lambda x: [store.put(ti.text, chars={str(i): {"이름": f"캐릭터 {i}", "레벨": "1"} for i in range(1, 7)}), p.dismiss(), self.refresh()])
        p.open()

# --- [3단계: 캐릭터 선택 화면 - 6개 슬롯 구현] ---
class CharSelect(Screen):
    def on_enter(self):
        self.clear_widgets()
        acc = self.manager.current_acc
        data = store.get(acc)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(SLabel(text=f"[{acc}] 캐릭터 선택", size_hint_y=0.1, font_size='20sp'))
        
        # 🛠️ 그리드 생성
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.8)
        chars = data.get('chars', {})
        
        for i in range(1, 7):
            char_info = chars.get(str(i), {"이름": f"빈 캐릭터 {i}", "레벨": "0"})
            btn = SBtn(text=f"{char_info['이름']}\nLv.{char_info['레벨']}", halign='center')
            btn.bind(on_release=lambda x, slot=i: self.go_detail(slot))
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        
        back = SBtn(text="뒤로가기", size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1))
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back)
        self.add_widget(layout)

    def go_detail(self, slot):
        self.manager.current_slot = slot
        # 상세 페이지 이동 로직 (추후 구현)
        print(f"Slot {slot} 클릭됨")

class PristonApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.current_acc = ""
        sm.current_slot = 0
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharSelect(name='char_select'))
        return sm

if __name__ == '__main__':
    PristonApp().run()
