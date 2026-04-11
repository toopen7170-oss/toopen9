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

# [보완] 폰트 로딩 방식 수정: 파일이 없으면 아예 무시해서 튕김 방지
FONT_NAME = "Roboto" # 기본값
if os.path.exists("font.ttf"):
    try:
        LabelBase.register(name="KFont", fn_regular="font.ttf")
        FONT_NAME = "KFont"
    except:
        pass

store = JsonStore('pt1_save_data.json')

class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.font_name = FONT_NAME
        self.size_hint_y = None
        self.height = 120

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.font_name = FONT_NAME

class CharDetail(Screen):
    def on_enter(self):
        self.refresh_ui()

    def refresh_ui(self):
        self.clear_widgets()
        acc = getattr(self.manager, 'current_acc', 'Default')
        slot = getattr(self.manager, 'current_slot', '1')
        
        # 데이터 안전하게 가져오기
        if not store.exists(acc): store.put(acc, chars={})
        acc_data = store.get(acc)
        char_data = acc_data.get('chars', {}).get(slot, {"items": []})

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(SLabel(text=f"[{acc}] 캐릭터 {slot} 상세내용", size_hint_y=0.1))

        # 인벤토리 무한 줄 추가 영역
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        for idx, text in enumerate(char_data.get('items', [])):
            row = BoxLayout(size_hint_y=None, height=120, spacing=5)
            ti = TextInput(text=text, font_name=FONT_NAME, multiline=False, padding_y=[20, 10])
            s_b = Button(text="저장", size_hint_x=0.2, font_name=FONT_NAME)
            d_b = Button(text="삭제", size_hint_x=0.2, font_name=FONT_NAME, background_color=(1,0,0,1))
            
            s_b.bind(on_release=lambda x, i=idx, t=ti: self.save_item(acc, slot, i, t.text))
            d_b.bind(on_release=lambda x, i=idx: self.confirm_del(acc, slot, i))
            
            row.add_widget(ti); row.add_widget(s_b); row.add_widget(d_b)
            self.grid.add_widget(row)

        self.scroll.add_widget(self.grid)
        layout.add_widget(self.scroll)

        # 하단 버튼들
        add_b = SBtn(text="+ 인벤토리 줄 추가", background_color=(0, 0.7, 0.3, 1))
        add_b.bind(on_release=lambda x: self.add_row(acc, slot))
        layout.add_widget(add_b)

        back = SBtn(text="뒤로가기", background_color=(0.5, 0.5, 0.5, 1))
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back)

        self.add_widget(layout)

    def add_row(self, acc, slot):
        data = store.get(acc)
        if slot not in data['chars']: data['chars'][slot] = {"items": []}
        data['chars'][slot]['items'].append("")
        store.put(acc, **data)
        self.refresh_ui()
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def save_item(self, acc, slot, idx, text):
        data = store.get(acc)
        data['chars'][slot]['items'][idx] = text
        store.put(acc, **data)
        Popup(title="알림", content=SLabel(text="저장되었습니다."), size_hint=(0.6, 0.2)).open()

    def confirm_del(self, acc, slot, idx):
        c = BoxLayout(orientation='vertical', padding=10)
        c.add_widget(SLabel(text="정말 삭제하시겠습니까?"))
        b = SBtn(text="삭제하기", background_color=(1,0,0,1))
        pop = Popup(title="확인", content=c, size_hint=(0.7, 0.3))
        def do_del(x):
            data = store.get(acc)
            data['chars'][slot]['items'].pop(idx)
            store.put(acc, **data)
            self.refresh_ui(); pop.dismiss()
        b.bind(on_release=do_del); c.add_widget(b); pop.open()

class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        l = BoxLayout(orientation='vertical', padding=20)
        l.add_widget(SLabel(text="PT1 Manager 실행 성공", font_size='20sp'))
        btn = SBtn(text="캐릭터 관리 시작", background_color=(0.2, 0.5, 0.8, 1))
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'char_detail'))
        l.add_widget(btn); self.add_widget(l)

class PT1App(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(CharDetail(name='char_detail'))
        return sm

if __name__ == '__main__':
    PT1App().run()
