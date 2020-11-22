import kivy
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty,ListProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
import random

class MainWindow(Screen):
    pass

class modal_view(ModalView):

    def try_again(instance,par):
        par.manager.current="second"
        par.manager.transition.direction="left"
    def main_page(instance,par):
        par.manager.current="main"
        par.manager.transition.direction="left"

class modal_view_2(ModalView):
    def try_again(instance,par):
        par.manager.current="Fourth"
        par.manager.transition.direction="left"

    def main_page(instance,par):
        par.manager.current="main"
        par.manager.transition.direction="left"

def show_modal(result):
    instance=modal_view()
    instance.ids.result.text=result
    instance.open()

def show_modal_2(result):
    instance=modal_view_2()
    instance.ids.result.text=result
    instance.open()

randomList=[]
f=open('words.txt','r')
words=[line.rstrip('\n') for line in f]
f.close()

class SecondWindow(Screen):
    
    def on_start(self):
        self.repeat=Clock.schedule_interval(self.update_label,1.5)
        Clock.schedule_once(self.stop,int(self.ids.number.text)*1.5+1)

    def stop(self,dt):
        self.repeat.cancel()
        self.ids.number.text=""
        self.ids.content2.text=""
        self.manager.current="Third"
        self.manager.transition.direction="left"
        
    def update_label(self,dt):
        randomWord=random.choice(words)
        self.ids.content2.text=randomWord
        randomList.append(randomWord)
        
class ThirdWindow(Screen):
    second=ObjectProperty()

    def validate(self):
        if self.ids.answer3.text.rsplit("\n") ==randomList:
            randomList.clear()
            show_modal('correct')
        else:
            randomList.clear()
            show_modal('wrong')
            
colors=[ '#5ac18e','#ffff66']
green=[]
yellow=[]
class FourthWindow(Screen):
    def color_pattern(self):
        layout = GridLayout(cols=4,rows=4,size_hint=(.4,.4),pos_hint={'center_x':.5,'y':.2})
        for i in range(1,17):
            l=Label(text=str(i))
            r=random.randint(0,1)
            s=kivy.utils.get_color_from_hex(colors[r])
            if(r==0):green.append(i)
            else:yellow.append(i)
            with l.canvas.before:
                Color(s[0],s[1],s[2],s[3])
                l.rect = Rectangle(pos=l.pos, size=l.size)
                def update_rect(instance, value):
                    instance.rect.pos = instance.pos
                    instance.rect.size = instance.size
                l.bind(pos=update_rect, size=update_rect)
            layout.add_widget(l)
        self.add_widget(layout)
        Clock.schedule_once(self.go_to_fifth,3)
    def go_to_fifth(self,dt):
        self.manager.current="Fifth"
        self.manager.transition.direction="left"
        
class FifthWindow(Screen):
    def validate_pattern(self):
        c1=[int(i) for i in self.ids.color_1.text.rsplit("\n") if i!='']
        c1.sort()
        green.sort()
        c2=[int(i) for i in self.ids.color_2.text.rsplit("\n") if i!='']
        c2.sort()
        yellow.sort()
        if (c1==green and
            c2 ==yellow) :
            green.clear()
            yellow.clear()
            show_modal_2('correct')
        else:
            green.clear()
            yellow.clear()
            show_modal_2('wrong')
    
class WindowManager(ScreenManager):
    pass

kv=Builder.load_file("gui.kv")

class MyMainApp(App):
    def build(self):
        return kv
        
if __name__ == "__main__":
    MyMainApp().run()
