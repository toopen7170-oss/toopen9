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

# --- [폰트 강제 적용 로직] ---
# 파일 이름이 font.ttf 인지 Font.ttf 인지 확인이 필요할 수 있어 두 경우 모두 체크합니다.
FONT_FILE = "font.ttf"
if not os.path.exists(FONT_FILE) and os.path.exists("Font.ttf"):
    FONT_FILE = "Font.ttf"

if os.path.exists(FONT_FILE):
    try:
        LabelBase.register(name="KFont", fn_regular=FONT_FILE)
        # 앱 전체의 기본 폰트를 KFont로 강제 고정
        Config.set('kivy', 'default_font', ['KFont', FONT_FILE, FONT_FILE, FONT_FILE])
        MY_FONT = "KFont"
    except:
        MY_FONT = None
else:
    MY_FONT = None

store = JsonStore('pt1_manager.json')

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
        self.padding_y = [25, 10] # 줄 밑에 쓰게 위치 조정

# --- 캐릭터 상세 화면 (인벤토리 + 다중 사진) ---
class CharDetail(Screen):
    def on_enter(self): self.refresh_ui()

    def refresh_ui(self):
        self.clear_widgets()
        acc = getattr(self.manager, 'current_acc', 'DefaultAcc')
        slot = getattr(self.manager, 'current_slot', '1')
        
        if not store.exists(acc): store.put(acc, chars={})
        char_data = store.get(acc).get('chars', {}).get(slot, {"items": [], "photos": []})

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(SLabel(text=f"[{acc}] 캐릭터 {slot} 상세내용", font_size='20sp', size_hint_y=0.1))

        # 인벤토리 (무한 줄)
        self.scroll = ScrollView(size_hint_y=0.5)
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        for idx, text in enumerate(char_data.get('items', [])):
            row = BoxLayout(size_hint_y=None, height=120, spacing=5)
            ti = SInput(text=text, multiline=False)
            s_b = Button(text="저장", size_hint_x=0.2); d_b = Button(text="삭제", size_hint_x=0.2, background_color=(1,0,0,1))
            if MY_FONT: s_b.font_name = MY_FONT; d_b.font_name = MY_FONT
            
            s_b.bind(on_release=lambda x, i=idx, t=ti: self.save_item(acc, slot, i, t.text))
            d_b.bind(on_release=lambda x, i=idx: self.confirm_del(acc, slot, i))
            
            row.add_widget(ti); row.add_widget(s_b); row.add_widget(d_b)
            self.grid.add_widget(row)
        
        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)

        # 사진 및 추가 버튼
        btn_grid = GridLayout(cols=2, size_hint_y=0.3, spacing=10)
        add_row_b = SBtn(text="+ 인벤토리 줄 추가", background_color=(0, 0.7, 0.3, 1))
        add_row_b.bind(on_release=lambda x: self.add_row(acc, slot))
        
        photo_add_b = SBtn(text="사진 추가", background_color=(0.1, 0.5, 0.8, 1))
        photo_add_b.bind(on_release=self.ask_photo)
        
        photo_del_b = SBtn(text="사진 삭제", background_color=(0.7, 0.1, 0.1, 1))
        photo_del_b.bind(on_release=self.confirm_photo_del)

        back_b = SBtn(text="뒤로가기")
        back_b.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))

        btn_grid.add_widget(add_row_b); btn_grid.add_widget(photo_add_b)
        btn_grid.add_widget(photo_del_b); btn_grid.add_widget(back_b)
        layout.add_widget(btn_grid)

        self.add_widget(layout)

    def add_row(self, acc, slot):
        d = store.get(acc)
        if slot not in d['chars']: d['chars'][slot] = {"items": [], "photos": []}
        d['chars'][slot]['items'].append("")
        store.put(acc, **d)
        self.refresh_ui()
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def save_item(self, acc, slot, idx, text):
        d = store.get(acc)
        d['chars'][slot]['items'][idx] = text
        store.put(acc, **d)
        Popup(title="성공", content=SLabel(text="저장되었습니다."), size_hint=(0.6, 0.2)).open()

    def confirm_del(self, acc, slot, idx):
        self.show_pop("줄을 삭제하시겠습니까?", lambda: self.do_del(acc, slot, idx))

    def ask_photo(self, *a):
        self.show_pop("갤러리 사진 추가 권한을 허용하시겠습니까?", self.refresh_ui)

    def confirm_photo_del(self, *a):
        self.show_pop("선택한 사진을 삭제하시겠습니까?", self.refresh_ui)

    def do_del(self, acc, slot, idx):
        d = store.get(acc)
        d['chars'][slot]['items'].pop(idx)
        store.put(acc, **d); self.refresh_ui()

    def show_pop(self, msg, yes_func):
        c = BoxLayout(orientation='vertical', padding=10, spacing=10)
        c.add_widget(SLabel(text=msg))
        b = SBtn(text="확인", background_color=(1,0,0,1))
        pop = Popup(title="확인", content=c, size_hint=(0.8, 0.4))
        b.bind(on_release=lambda x: [yes_func(), pop.dismiss()])
        c.add_widget(b); pop.open()

class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=20)
        l.add_widget(SLabel(text="PT1 Manager", font_size='30sp'))
        b = SBtn(text="시작하기", background_color=(0.2, 0.6, 1, 1))
        b.bind(on_release=lambda x: setattr(self.manager, 'current', 'char_detail'))
        l.add_widget(b); self.add_widget(l)

class PT1App(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharDetail(name='char_detail'))
        return sm

if __name__ == '__main__':
    PT1App().run()
