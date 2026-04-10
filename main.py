from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.text import LabelBase

# 폰트 등록
LabelBase.register(name='CustomFont', fn_regular='font.ttf')

class PristonTaleApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # 배경 이미지 (bg.png)
        bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False)
        
        # 내부 이미지 (images.jpeg)
        inner_img = Image(source='images.jpeg', size_hint=(1, 0.5))
        
        # 폰트 적용된 라벨
        txt = Label(text='PristonTale Mobile\n빌드 테스트 중', 
                    font_name='CustomFont', 
                    font_size='24sp',
                    size_hint=(1, 0.2))

        layout.add_widget(bg)
        layout.add_widget(inner_img)
        layout.add_widget(txt)
        return layout

if __name__ == '__main__':
    PristonTaleApp().run()
