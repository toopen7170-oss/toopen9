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

#
FONT_PATH = "font.ttf"
FONT_NAME = "KoreanFont"
if os.path.exists(FONT_PATH):
    LabelBase.register(name=FONT_NAME, fn_regular=FONT_PATH)
else:
    FONT_NAME = "Roboto"

store = JsonStore('pt1_data.json')

class SLabel(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.font_name = FONT_NAME

class SBtn(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.font_name = FONT_NAME
        self.size_hint_y = None
        self.height = 100

class CharDetail(Screen):
    def on_enter(self):
        self.refresh_ui()

    def refresh_ui(self):
        self.clear_widgets()
        acc = self.manager.current_acc
        slot = self.manager.current_slot
        self.data = store.get(acc)['chars'].get(slot, {"items": [], "photos": []})
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 1. 인벤토리 영역 (무한 줄 추가)
        main_layout.add_widget(SLabel(text="[인벤토리]", size_hint_y=0.05))
        self.item_scroll = ScrollView(size_hint_y=0.4)
        self.item_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.item_grid.bind(minimum_height=self.item_grid.setter('height'))
        
        for idx, item_text in enumerate(self.data.get('items', [])):
            self.add_item_row(idx, item_text)
            
        self.item_scroll.add_widget(self.item_grid)
        main_layout.add_widget(self.item_scroll)
        
        add_item_btn = SBtn(text="+ 인벤토리 줄 추가", background_color=(0, 0.7, 0.3, 1))
        add_item_btn.bind(on_release=self.append_new_item)
        main_layout.add_widget(add_item_btn)

        # 2. 사진 영역 (여러 장 관리)
        main_layout.add_widget(SLabel(text="[캐릭터 사진]", size_hint_y=0.05))
        self.photo_scroll = ScrollView(size_hint_y=0.2)
        self.photo_grid = GridLayout(rows=1, spacing=10, size_hint_x=None)
        self.photo_grid.bind(minimum_width=self.photo_grid.setter('width'))
        
        for p_path in self.data.get('photos', []):
            p_btn = Button(text="사진", size_hint=(None, None), size=(150, 150))
            p_btn.bind(on_release=lambda x, p=p_path: self.confirm_delete_photo(p))
            self.photo_grid.add_widget(p_btn)
            
        self.photo_scroll.add_widget(self.photo_grid)
        main_layout.add_widget(self.photo_scroll)

        p_controls = BoxLayout(size_hint_y=0.1, spacing=5)
        p_add = SBtn(text="사진 추가", background_color=(0.2, 0.5, 0.8, 1))
        p_add.bind(on_release=self.ask_photo_permission)
        p_controls.add_widget(p_add)
        main_layout.add_widget(p_controls)

        # 하단 메뉴
        back_btn = SBtn(text="뒤로가기", height=120)
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'char_select'))
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)

    def add_item_row(self, idx, text):
        row = BoxLayout(size_hint_y=None, height=100, spacing=5)
        ti = TextInput(text=text, font_name=FONT_NAME, multiline=False)
        s_btn = Button(text="저장", size_hint_x=0.2, font_name=FONT_NAME)
        d_btn = Button(text="삭제", size_hint_x=0.2, font_name=FONT_NAME, background_color=(0.8, 0.2, 0.2, 1))
        
        s_btn.bind(on_release=lambda x: self.save_single_item(idx, ti.text))
        d_btn.bind(on_release=lambda x: self.confirm_delete_item(idx))
        
        row.add_widget(ti); row.add_widget(s_btn); row.add_widget(d_btn)
        self.item_grid.add_widget(row)

    def append_new_item(self, *a):
        self.data['items'].append("")
        self.update_store()
        self.refresh_ui()
        Clock.schedule_once(lambda dt: setattr(self.item_scroll, 'scroll_y', 0), 0.1) #

    def save_single_item(self, idx, text):
        self.data['items'][idx] = text
        self.update_store()
        Popup(title="알림", content=SLabel(text="저장되었습니다."), size_hint=(0.6, 0.2)).open()

    def confirm_delete_item(self, idx):
        self.show_confirm("줄을 삭제하시겠습니까?", lambda: self.delete_item(idx))

    def delete_item(self, idx):
        self.data['items'].pop(idx)
        self.update_store()
        self.refresh_ui()

    def ask_photo_permission(self, *a):
        self.show_confirm("갤러리 접근을 허용하시겠습니까?", self.refresh_ui)

    def confirm_delete_photo(self, path):
        self.show_confirm("사진을 삭제하시겠습니까?", self.refresh_ui)

    def show_confirm(self, msg, yes_func):
        c = BoxLayout(orientation='vertical', padding=10, spacing=10)
        c.add_widget(SLabel(text=msg))
        btns = BoxLayout(size_hint_y=0.4, spacing=10)
        y = SBtn(text="확인"); n = SBtn(text="취소")
        btns.add_widget(y); btns.add_widget(n); c.add_widget(btns)
        pop = Popup(title="확인", content=c, size_hint=(0.8, 0.4))
        y.bind(on_release=lambda x: [yes_func(), pop.dismiss()])
        n.bind(on_release=pop.dismiss); pop.open()

    def update_store(self):
        acc = self.manager.current_acc
        slot = self.manager.current_slot
        all_data = store.get(acc)
        all_data['chars'][slot] = self.data
        store.put(acc, **all_data)

class PT1App(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        # (MainMenu, CharSelect 클래스는 이전과 동일하므로 생략하거나 기존 코드 유지)
        sm.add_widget(CharDetail(name='char_detail'))
        return sm

if __name__ == '__main__':
    PT1App().run()
