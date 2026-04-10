from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.text import LabelBase

# 폰트 등록
LabelBase.register(name='CustomFont', fn_regular='font.ttf')

class PristonTaleApp(App):
    def build(self):
        # 전체를 담는 레이아웃
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # 1. 배경 이미지 (새로 추가하신 bg1.png)
        bg = Image(source='bg1.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 0.4))
        
        # 2. 중간 이미지 레이아웃 (images1, images2를 가로로 배치)
        mid_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.4))
        img1 = Image(source='images1.jpg')
        img2 = Image(source='images2.jpg')
        mid_layout.add_widget(img1)
        mid_layout.add_widget(img2)
        
        # 3. 폰트 적용된 하단 문구
        txt = Label(text='PristonTale Mobile\n[ 이미지/폰트 업데이트 완료 ]', 
                    font_name='CustomFont', 
                    font_size='22sp',
                    halign='center',
                    size_hint=(1, 0.2))

        layout.add_widget(bg)
        layout.add_widget(mid_layout)
        layout.add_widget(txt)
        return layout

if __name__ == '__main__':
    PristonTaleApp().run()
