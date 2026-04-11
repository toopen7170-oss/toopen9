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
from kivy.uix.image import Image

# --- [1단계: 기본 설정] ---
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

# --- [2단계: 메인 메뉴] ---
class MainMenu(Screen):
    def on_enter(self): self.refresh()
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(SLabel(text="[PT1 통합 검색]", font_size='22sp', size_hint_y=0.1))
        
        # 검색창
        s_box = BoxLayout(size_hint_y=None, height=120, spacing=5)
        self.stti = TextInput(hint_text="검색어 입력...", multiline=False)
        if DF: self.stti.font_name = DF
        s_btn = Button(text="검색", size_hint_x=0.25, background_color=(0.2, 0.6, 1, 1))
        if DF: s_btn.font_name = DF
        s_btn.bind(on_release=self.refresh)
        s_box.add_widget(self.stti); s_box.add_widget(s_btn); layout.add_widget(s_box)

        # 계정 생성 버튼
        add_btn = SBtn(text="+ 새 계정 만들기", background_color=(0.1, 0.7, 0.3, 1))
        add_btn.bind(on_release=self.add_pop)
        layout.add_widget(add_btn)

        # 목록
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
                
                del_btn = Button(text="X", size_hint_x=0.2, background_color=(0.8, 0.2, 0.2, 1))
                if DF: del_btn.font_name = DF
                del_btn.bind(on_release=lambda x, name=k: self.confirm_del(name))
                row.add_widget(acc_btn); row.add_widget(del_btn); self.grid.add_widget(row)

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
        def save(x):
            if ti.text.strip():
                store.put(ti.text.strip(), chars={str(i): {"이름": f"캐릭터 {i}", "레벨": "1", "직업": "파이터"} for i in range(1, 7)})
                p.dismiss(); self.refresh()
        b.bind(on_release=save); p.open()

# --- [3단계: 캐릭터 선택 화면] ---
class CharSelect(Screen):
    def on_enter(self):
        self.clear_widgets()
        acc = self.manager.current_acc
        data = store.get(acc)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(SLabel(text=f"[{acc}] 캐릭터 선택", size_hint_y=0.1, font_size='20sp'))
        
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.8)
        chars = data.get('chars', {})
        for i in range(1, 7):
            char_info = chars.get(str(i), {"이름": f"빈 캐릭터 {i}", "레벨": "0"})
            btn = SBtn(text=f"{char_info['이름']}\nLv.{char_info['레벨']}", halign='center')
            btn.bind(on_release=lambda x, slot=str(i): self.go_detail(slot))
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        back = SBtn(text="뒤로가기", size_hint_y=0.1, background_color=(0.5, 0.5, 0.5, 1))
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back)
        self.add_widget(layout)

    def go_detail(self, slot):
        self.manager.current_slot = slot
        self.manager.current = 'char_detail'

# --- [4단계: 캐릭터 상세 수정 화면] ---
class CharDetail(Screen):
    def on_enter(self):
        self.clear_widgets()
        acc = self.manager.current_acc
        slot = self.manager.current_slot
        char_data = store.get(acc)['chars'][slot]
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 상단 정보 (이름/레벨 수정 가능)
        top = BoxLayout(size_hint_y=None, height=120, spacing=10)
        self.name_in = TextInput(text=char_data.get('이름', ''), multiline=False)
        self.lv_in = TextInput(text=char_data.get('레벨', ''), multiline=False)
        if DF: self.name_in.font_name = DF; self.lv_in.font_name = DF
        top.add_widget(SLabel(text="이름:", size_hint_x=0.2))
        top.add_widget(self.name_in)
        top.add_widget(SLabel(text="Lv:", size_hint_x=0.15))
        top.add_widget(self.lv_in)
        layout.add_widget(top)
        
        # 버튼 영역
        btns = BoxLayout(size_hint_y=0.2, spacing=10)
        save_btn = SBtn(text="저장", background_color=(0.1, 0.5, 0.8, 1))
        save_btn.bind(on_release=self.save_data)
        back_btn = SBtn(text="뒤로", background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'char_select'))
        btns.add_widget(save_btn); btns.add_widget(back_btn)
        layout.add_widget(btns)
        
        self.add_widget(layout)

    def save_data(self, *a):
        acc = self.manager.current_acc
        slot = self.manager.current_slot
        full_data = store.get(acc)
        full_data['chars'][slot]['이름'] = self.name_in.text
        full_data['chars'][slot]['레벨'] = self.lv_in.text
        store.put(acc, **full_data)
        Popup(title="성공", content=SLabel(text="저장되었습니다."), size_hint=(0.6, 0.3)).open()

class PristonApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.current_acc = ""; sm.current_slot = "1"
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharSelect(name='char_select'))
        sm.add_widget(CharDetail(name='char_detail'))
        return sm

if __name__ == '__main__':
    PristonApp().run()
