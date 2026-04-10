import os
import sys
import traceback
from plyer import share
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

def logger(type, value, tb):
    log_content = "".join(traceback.format_exception(type, value, tb))
    temp_path = os.path.join(os.path.dirname(__file__), "error_log.txt")
    with open(temp_path, "w", encoding='utf-8') as f:
        f.write("--- PT1 Manager Error Log ---\n" + log_content)
    try: share.share(temp_path)
    except: pass
sys.excepthook = logger

KV = '''
ScreenManager:
    MainScreen:
<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'PT1 Manager (준비완료)'
            font_size: 30
'''
class MainScreen(Screen): pass
class PT1ManagerApp(App):
    def build(self): return Builder.load_string(KV)
if __name__ == '__main__': PT1ManagerApp().run()
