#!/usr/bin/env python

import kivy
kivy.require('1.9.1')

import os

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemLabel
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter

import passInterface

class RootScreen(GridLayout):

    PASS_SCREEN = "pass_screen"
    SETUP_SCREEN = "setup_screen"

    def __init__(self, app, **kwargs):
        super(RootScreen, self).__init__(**kwargs)
        self.app = app
        self.cols = 1
        self.setup_screen = SetupScreen(self)
        self.pass_screen = None
        self.add_widget(self.setup_screen)

    def switch_screen(self, target):
        if target == RootScreen.PASS_SCREEN:
            self.pass_screen = PassScreen(self, self.setup_screen.path.text)
            self.clear_widgets()
            self.add_widget(self.pass_screen)
        elif target == RootScreen.SETUP_SCREEN:
            self.clear_widgets()
            self.add_widget(self.setup_screen)

class PassScreen(GridLayout):

    def __init__(self, root, pass_dir, **kwargs):
        super(PassScreen, self).__init__(**kwargs)
        self.root = root
        self.cols = 1
        self.passwords = []
        self.get_passwords(pass_dir)

        # ListView is going to become deprecated
        # but it's replacement (RecycleView) is currently
        # not stable / usable
        self.list_adapter = ListAdapter(selection_mode = 'single', allow_empty_selection=False, data=self.passwords, cls=ListItemButton)
        self.pass_list = ListView(adapter=self.list_adapter)
        self.add_widget(self.pass_list)

        self.pass_label = Label(text='...')
        self.add_widget(self.pass_label)

        self.button_space = GridLayout()
        self.button_space.cols = 2
        leaveButton = Button(text = 'Exit')
        leaveButton.bind(on_press=self.leave)
        showButton = Button(text = 'Show')
        showButton.bind(on_press=self.show)

        self.button_space.add_widget(leaveButton)
        self.button_space.add_widget(showButton)
        self.add_widget(self.button_space)

    def get_passwords(self, root):
        self.passwords = passInterface.get_passwords(root)

    def leave(self, instance):
        self.root.app.stop()

    def show(self, instance):
        if self.list_adapter.selection != []:
            self.pass_label.text = passInterface.get_password(self.list_adapter.selection[0].text)

class SetupScreen(GridLayout):

    def __init__(self, root, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)
        self.root = root
        self.cols = 1
        self.add_widget(Label(text='Please enter the location of your .password-store directory'))
        self.path = TextInput(multiline=False, text=os.path.join(os.environ['HOME'], '.password-store'))
        self.add_widget(self.path)
        done = Button(text='Ok')
        done.bind(on_press=self.done)
        self.add_widget(done)

    def done(self, instance):
        self.root.switch_screen(RootScreen.PASS_SCREEN)

class MyApp(App):
    def build(self):
        return RootScreen(self)

if __name__ == '__main__':
    MyApp().run()
