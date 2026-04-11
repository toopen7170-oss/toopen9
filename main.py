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

# --- [폰트 설정: 어떤 상황에도 튕기지 않게] ---
FONT_FILE = "font.ttf"
MY_FONT = "KoreanFont"
if os.path.exists(FONT_FILE):
    try:
        LabelBase.register(name=MY_FONT, fn_regular=FONT_FILE)
        Config.set('kivy', 'default_font', [MY_FONT, FONT_FILE, FONT_FILE, FONT_FILE])
    except: MY_FONT = None
else:
    MY_FONT = None

store = JsonStore('pt1_final_v5.json')

class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        if MY_FONT: self.font_name = MY_FONT
        self.size_hint_y = None
        self.height = 110

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        if MY_FONT: self.font_name = MY_FONT

class SInput(TextInput):
    def __init__(self, **kw):
        super().__init__(**kw)
        if MY_FONT: self.font_name = MY_FONT
        self.size_hint_y = None
        self.height = 100
        self.multiline = False
        self.padding_y = [20, 10]

# --- [메인 화면: 계정 추가 및 이름 입력] ---
class MainMenu(Screen):
    def on_enter(self): self.refresh()
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        layout.add_widget(SLabel(text="[PT1 계정 목록]", font_size='22sp', size_hint_y=0.1))
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll = ScrollView(); scroll.add_widget(self.grid); layout.add_widget(scroll)
        add_btn = SBtn(text="+ 새 계정 추가 (이름 입력)", background_color=(0, 0.6, 0.3, 1))
        add_btn.bind(on_release=self.add_acc_pop)
        layout.add_widget(add_btn); self.add_widget(layout)

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

    def add_acc_pop(self, *a):
        c = BoxLayout(orientation='vertical', padding=10, spacing=10)
        ti = SInput(hint_text="계정 이름 입력")
        b = SBtn(text="생성"); c.add_widget(ti); c.add_widget(b)
        p = Popup(title="추가", content=c, size_hint=(0.8, 0.4))
        def save(x):
            if ti.text.strip():
                store.put(ti.text.strip(), detail={"job":"", "lv":""}, items=[])
                p.dismiss(); self.refresh()
        b.bind(on_release=save); p.open()

    def confirm_del(self, name):
        c = BoxLayout(orientation='vertical', padding=10)
        c.add_widget(SLabel(text=f"'{name}'\n삭제하시겠습니까?"))
        b = SBtn(text="확인 삭제", background_color=(1,0,0,1))
        pop = Popup(title="경고", content=c, size_hint=(0.7, 0.4))
        b.bind(on_release=lambda x: [store.delete(name), self.refresh(), pop.dismiss()]); c.add_widget(b); pop.open()

# --- [상세 화면: 세부내용 + 무한 인벤토리 + 사진] ---
class CharDetail(Screen):
    def on_enter(self): self.refresh_ui()
    def refresh_ui(self):
        self.clear_widgets()
        acc = getattr(self.manager, 'current_acc', '')
        if not acc: return
        data = store.get(acc)
        detail = data.get('detail', {"job":"", "lv":""})
        items = data.get('items', [])
        l = BoxLayout(orientation='vertical', padding=10, spacing=10)
        info = GridLayout(cols=2, size_hint_y=0.2, spacing=5)
        info.add_widget(SLabel(text="직업:")); self.job_ti = SInput(text=detail['job'])
        info.add_widget(self.job_ti)
        info.add_widget(SLabel(text="레벨:")); self.lv_ti = SInput(text=detail['lv'])
        info.add_widget(self.lv_ti); l.add_widget(info)
        l.add_widget(SLabel(text="[인벤토리]", size_hint_y=0.05))
        self.scroll = ScrollView(size_hint_y=0.45)
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        for idx, it in enumerate(items):
            row = BoxLayout(size_hint_y=None, height=110, spacing=5)
            ti = SInput(text=it)
            d_b = Button(text="X", size_hint_x=0.2, background_color=(0.8,0,0,1))
            if MY_FONT: d_b.font_name = MY_FONT
            d_b.bind(on_release=lambda x, i=idx: self.confirm_del(i))
            row.add_widget(ti); row.add_widget(d_b); self.grid.add_widget(row)
        self.scroll.add_widget(self.grid); l.add_widget(self.scroll)
        btns = GridLayout(cols=2, size_hint_y=0.3, spacing=10)
        save_b = SBtn(text="전체 저장", background_color=(0, 0.5, 0.8, 1))
        save_b.bind(on_release=self.save_all)
        add_b = SBtn(text="+ 줄 추가", background_color=(0, 0.7, 0.3, 1))
        add_b.bind(on_release=self.add_row)
        photo_b = SBtn(text="사진 폴더"); photo_b.bind(on_release=lambda x: self.pop("사진 기능을 준비 중입니다."))
        back_b = SBtn(text="뒤로가기"); back_b.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        btns.add_widget(save_b); btns.add_widget(add_b); btns.add_widget(photo_b); btns.add_widget(back_b)
        l.add_widget(btns); self.add_widget(l)

    def save_all(self, *a):
        acc = self.manager.current_acc
        new_items = [c.children[1].text for c in self.grid.children[::-1]]
        store.put(acc, detail={"job": self.job_ti.text, "lv": self.lv_ti.text}, items=new_items)
        self.pop("저장 완료!")

    def add_row(self, *a):
        acc = self.manager.current_acc
        d = store.get(acc); d['items'].append("")
        store.put(acc, **d); self.refresh_ui()
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def confirm_del(self, idx):
        c = BoxLayout(orientation='vertical', padding=10)
        c.add_widget(SLabel(text="삭제하시겠습니까?"))
        b = SBtn(text="삭제", background_color=(1,0,0,1))
        p = Popup(title="확인", content=c, size_hint=(0.7, 0.3))
        def do(x):
            acc = self.manager.current_acc
            d = store.get(acc); d['items'].pop(idx)
            store.put(acc, **d); self.refresh_ui(); p.dismiss()
        b.bind(on_release=do); c.add_widget(b); p.open()

    def pop(self, msg):
        Popup(title="알림", content=SLabel(text=msg), size_hint=(0.6, 0.2)).open()

class PT1App(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.current_acc = ""
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharDetail(name='char_detail'))
        return sm

if __name__ == '__main__':
    PT1App().run()
