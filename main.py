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
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.config import Config

# --- [1. 폰트 로드: 100% 적용 및 튕김 방지] ---
FONT_FILE = "font.ttf"
MY_FONT = "KoreanFont"
if os.path.exists(FONT_FILE):
    try:
        LabelBase.register(name=MY_FONT, fn_regular=FONT_FILE)
        Config.set('kivy', 'default_font', [MY_FONT, FONT_FILE, FONT_FILE, FONT_FILE])
    except: MY_FONT = None
else:
    MY_FONT = None

# 데이터 저장소 초기화
store = JsonStore('pt1_final_data.json')

# 공통 위젯 정의 (폰트 및 스타일 통일)
class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        if MY_FONT: self.font_name = MY_FONT
        self.size_hint_y = None
        self.height = 120

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        if MY_FONT: self.font_name = MY_FONT

class SInput(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        if MY_FONT: self.font_name = MY_FONT
        self.size_hint_y = None
        self.height = 110
        self.padding_y = [25, 10] #

# --- [2. 메인 화면: 계정 관리] ---
class MainMenu(Screen):
    def on_enter(self): self.refresh()
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.layout.add_widget(SLabel(text="[PT1 계정 목록]", font_size='22sp', size_hint_y=0.1))
        
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll = ScrollView()
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        
        self.add_acc_btn = SBtn(text="+ 새 계정 생성", background_color=(0, 0.6, 0.3, 1))
        self.add_acc_btn.bind(on_release=self.add_pop)
        self.layout.add_widget(self.add_acc_btn)
        self.add_widget(self.layout)

    def refresh(self, *a):
        self.grid.clear_widgets()
        for k in list(store.keys()):
            row = BoxLayout(size_hint_y=None, height=130, spacing=5)
            btn = SBtn(text=f"계정: {k}", size_hint_x=0.8)
            btn.bind(on_release=lambda x, n=k: self.go_detail(n))
            del_b = Button(text="X", size_hint_x=0.2, background_color=(0.8, 0, 0, 1))
            if MY_FONT: del_b.font_name = MY_FONT
            del_b.bind(on_release=lambda x, n=k: self.confirm_del(n))
            row.add_widget(btn); row.add_widget(del_b); self.grid.add_widget(row)

    def go_detail(self, name):
        self.manager.current_acc = name
        self.manager.current = 'char_detail'

    def confirm_del(self, name):
        c = BoxLayout(orientation='vertical', padding=15)
        c.add_widget(SLabel(text=f"'{name}'\n전체를 삭제하시겠습니까?"))
        b = SBtn(text="삭제", background_color=(0.8, 0, 0, 1))
        pop = Popup(title="최종 확인", content=c, size_hint=(0.8, 0.4))
        b.bind(on_release=lambda x: [store.delete(name), self.refresh(), pop.dismiss()]); c.add_widget(b); pop.open()

    def add_pop(self, *a):
        c = BoxLayout(orientation='vertical', padding=15, spacing=15)
        ti = SInput(hint_text="계정 이름 입력")
        b = SBtn(text="생성하기")
        c.add_widget(ti); c.add_widget(b); p = Popup(title="계정 추가", content=c, size_hint=(0.8, 0.4))
        def save(x):
            if ti.text.strip():
                store.put(ti.text.strip(), items=[])
                p.dismiss(); self.refresh()
        b.bind(on_release=save); p.open()

# --- [3. 상세 화면: 무한 인벤토리 & 사진 관리] ---
class CharDetail(Screen):
    def on_enter(self): self.refresh_ui()

    def refresh_ui(self):
        self.clear_widgets()
        acc = getattr(self.manager, 'current_acc', '')
        if not acc: return
        
        # 데이터 로드 (없으면 생성)
        if not store.exists(acc): store.put(acc, items=[])
        self.data = store.get(acc).get('items', [])
        
        main_l = BoxLayout(orientation='vertical', padding=15, spacing=15)
        main_l.add_widget(SLabel(text=f"[{acc}] 인벤토리", size_hint_y=0.05))
        
        # 무한 인벤토리 스크롤 영역
        self.scroll = ScrollView(size_hint_y=0.6)
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        for idx, text in enumerate(self.data):
            row = BoxLayout(size_hint_y=None, height=120, spacing=5)
            ti = SInput(text=text, multiline=False)
            s_b = Button(text="저장", size_hint_x=0.2); d_b = Button(text="삭제", size_hint_x=0.2, background_color=(0.8, 0.1, 0.1, 1))
            if MY_FONT: s_b.font_name = MY_FONT; d_b.font_name = MY_FONT
            
            s_b.bind(on_release=lambda x, i=idx, t=ti: self.save_item(i, t.text))
            d_b.bind(on_release=lambda x, i=idx: self.confirm_item_del(i))
            
            row.add_widget(ti); row.add_widget(s_b); row.add_widget(d_b); self.grid.add_widget(row)
        
        self.scroll.add_widget(self.grid); main_l.add_widget(self.scroll)
        
        # 제어 버튼 영역
        btns = GridLayout(cols=2, size_hint_y=0.25, spacing=10)
        add_b = SBtn(text="+ 줄 추가", background_color=(0, 0.7, 0.3, 1))
        add_b.bind(on_release=self.add_row)
        
        p_add = SBtn(text="사진 추가", background_color=(0.1, 0.5, 0.8, 1))
        p_add.bind(on_release=self.photo_pop)
        
        p_del = SBtn(text="사진 삭제", background_color=(0.7, 0, 0, 1))
        p_del.bind(on_release=self.photo_del_pop)
        
        back = SBtn(text="뒤로가기")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        
        btns.add_widget(add_b); btns.add_widget(p_add); btns.add_widget(p_del); btns.add_widget(back)
        main_l.add_widget(btns); self.add_widget(main_l)

    def add_row(self, *a):
        acc = self.manager.current_acc
        self.data.append("")
        store.put(acc, items=self.data)
        self.refresh_ui()
        #
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def save_item(self, idx, text):
        acc = self.manager.current_acc
        self.data[idx] = text
        store.put(acc, items=self.data)
        Popup(title="알림", content=SLabel(text="저장되었습니다."), size_hint=(0.6, 0.2)).open()

    def confirm_item_del(self, idx):
        self.show_pop("해당 줄을 삭제하시겠습니까?", lambda: self.do_del(idx))

    def photo_pop(self, *a):
        self.show_pop("사진 접근 권한을 허용하시겠습니까?", self.refresh_ui)

    def photo_del_pop(self, *a):
        self.show_pop("사진을 삭제하시겠습니까?", self.refresh_ui)

    def do_del(self, idx):
        acc = self.manager.current_acc
        self.data.pop(idx)
        store.put(acc, items=self.data)
        self.refresh_ui()

    def show_pop(self, msg, yes_func):
        c = BoxLayout(orientation='vertical', padding=15, spacing=15)
        c.add_widget(SLabel(text=msg))
        b = SBtn(text="확인", background_color=(0.8, 0, 0, 1))
        pop = Popup(title="확인", content=c, size_hint=(0.8, 0.4))
        b.bind(on_release=lambda x: [yes_func(), pop.dismiss()])
        c.add_widget(b); pop.open()

class PT1App(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.current_acc = ""
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharDetail(name='char_detail'))
        return sm

if __name__ == '__main__':
    PT1App().run()
