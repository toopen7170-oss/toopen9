import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.text import LabelBase

# 폰트 파일 존재 여부를 확인하고 등록합니다.
font_path = 'font.ttf'
if os.path.exists(font_path):
    LabelBase.register(name='CustomFont', fn_regular=font_path)
    DEFAULT_FONT = 'CustomFont'
else:
    DEFAULT_FONT = 'Roboto' # 폰트 없을 시 기본 폰트로 대체하는 안전장치

class PristonTaleApp(App):
    def build(self):
        # 레이아웃을 FloatLayout으로 변경하여 이미지를 겹치게(배경처럼) 만듭니다.
        root = FloatLayout()
        
        # 1. 배경 이미지 (화면 전체 꽉 차게)
        bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False)
        root.add_widget(bg)
        
        # 2. 내부 삽입 이미지 (화면 중앙 상단 배치)
        if os.path.exists('images.jpeg'):
            inner_img = Image(source='images.jpeg', 
                              size_hint=(0.8, 0.4),
                              pos_hint={'center_x': 0.5, 'top': 0.8})
            root.add_widget(inner_img)
        
        # 3. 텍스트 라벨 (하단 배치, 폰트 적용)
        txt = Label(text='PristonTale Mobile\nReady for Service', 
                    font_name=DEFAULT_FONT, 
                    font_size='22sp',
                    color=(1, 1, 0, 1), # 황금색으로 변경 (가독성 향상)
                    size_hint=(1, 0.2),
                    pos_hint={'center_x': 0.5, 'y': 0.1})
        root.add_widget(txt)
        
        return root

if __name__ == '__main__':
    PristonTaleApp().run()
