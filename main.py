import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import threading
from random import randrange
from kivy.clock import Clock, mainthread
from dependancies import portalAccess
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from hoverable import HoverBehavior
import os
# Window.borderless=True
if not os.path.exists("./loggedIn.ask"):
    with open("./loggedIn.ask","w")as ask:
        ask.write("False")

class SideNav(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.loadItems)
    def loadItems(self,args):
        # everpresent menu items---Name, Home, Performance, settings---
        main_child = self.children[0]
        fixed_items = ["Home","Performance","Library"]

        for i in fixed_items:
            print("yeah")

            item = Item()
            item._text="    "+i
            item._source = "./dependancies/"+i.lower()+".png"
            main_child.add_widget(item)
        main_child.add_widget(BoxLayout());
    pass
class Days(BoxLayout,HoverBehavior):
    pass
class Arrow(Image,HoverBehavior):
    pass
class ClassTemplate(BoxLayout,HoverBehavior):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.randomise_color,0)
        tuples = [(92 / 255, 299 / 255, 250 / 255, 1),(255/255, 89/255, 167/255,1),(213/255, 46/255, 1,1),(1, 252/255, 74/255,1)]
        rand_int = randrange(4)
        self._tuple =tuples[rand_int]

    def randomise_color(self,dt):



        pass
    pass

class RightSideIcon(Image,ButtonBehavior,HoverBehavior):
    pass
class RightSideNav(BoxLayout):
    pass

class MenuItem(BoxLayout,ButtonBehavior,HoverBehavior):

    pass
class screenManager(ScreenManager):
    pass


class CloseMinArea(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CustomInput(TextInput):
    pass

class SideBar(BoxLayout):
    pass

class MainScreen(Screen, BoxLayout):
    info_f=""
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.load,0)
#         check info and call screen necessary
    def load(self,dt):
        with open(portalAccess.absolutepath + "mation.cmt", "r") as info_f:
            info_f = eval(str(info_f.read()))
        courses = info_f["courses"]
        for key in dict(courses).keys():
            print(key)

        layout = self.ids._classes



class ButtonImage(Image, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # call login attempt
            self.parent.parent.parent.login()
        else:
            return False
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.container=BoxLayout(orientation="vertical",pos_hint={'center_x':.5, 'center_y':.5},size_hint=(None,None))
        # self.studentId=CustomInput(size_hint=(None,None),size=(dp(200),dp(30)))
        # self.password=CustomInput(size_hint=(None,None),size=(dp(200),dp(30)))
        # self.textButton = Button(text="Log In", id="login")
        #
        #
        # self.container.add_widget(self.studentId);self.container.add_widget(self.password);self.add_widget(self.textButton)
        # # self.textButton.bind(on_press=t)
        # self.add_widget(self.container)
        with open("./loggedIn.ask","r")as ask:
            if eval(ask.read()):
                Clock.schedule_once(self.change_screen,0)

    def change_screen(self,dt):
        self.parent.current = "main"
    def login(self):
        threading.Thread(target=self.login_attempt).start()

    # @mainthread
    def login_attempt(self):
        # TODO
        # fix auth
        s_id = self.ids.student_id.text
        password = self.ids.password.text

        if portalAccess.auth(portalAccess.login,portalAccess.studentPortal,s_id,password)[0] == "success":
            ass = portalAccess.getAssignments(); reg = portalAccess.getRegistrationData(); ca=portalAccess.getCaData()
            if ass=="success" and reg == "success" and ca == "success":
    #             go to next screen
                with open("./loggedIn.ask","w")as ask:
                    ask.write("True")

                self.parent.current="main"
            else:

                functions = [ass,reg,ca]
                for i in functions:
                    print(i)


        else:
            print("faileddd")


    pass
class Item(BoxLayout,HoverBehavior):
    pass

class Classmate(App):
    def build(self):

        return screenManager()



if __name__ == "__main__":
    Classmate().run()
