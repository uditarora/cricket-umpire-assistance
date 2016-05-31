# Kivy libraries
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window
import subprocess
import os

Window.size = (1280, 720)

Builder.load_file('layout.kv')

# Main Menu Screen with options to choose an OS Algorithm
class MainMenuScreen(Screen):

    slide_flag = "0"
    action_flag = "0"
    vflag = "0"

    # Show filename in fname_label
    def selected(self, filename, *args):
        # print "File selected: "+str(filename)
        fname_label = self.manager.get_screen('menu').fname_label
        if len(filename) > 0:
            fname_label.text = str(filename[0])
        else:
            fname_label.text = ''

    # Open the selected video
    def open(self, path, filename, *args):
        # print "Path: {}, filename: {}".format(path,filename)
        if len(filename) > 0:
            subprocess.call(["open", filename[0]])

    def set_action(self, text, *args):
        if text == "Fast":
            self.action_flag = "0"
        elif text == "Spin":
            self.action_flag = "1"
        else:
            self.action_flag = "2"

    def toggle_sliding(self, state, *args):
        if state == "down":
            self.slide_flag = "1"
        else:
            self.slide_flag = "0"

    # Run ballTracking.py
    def analyze(self, filename, *args):
        if len(filename) == 0:
            return
        if '171638.mp4' in filename[0]:
            self.vflag = "1"
        elif '171258.mp4' in filename[0]:
            self.vflag = "2"
        elif '171901.mp4' in filename[0]:
            self.vflag = "3"
        elif '171602.mp4' in filename[0]:
            self.vflag = "4"
        elif '171200.mp4' in filename[0]:
            self.vflag = "5"
        python_bin = "/Users/udit/.virtualenvs/cv/bin/python"
        script_path = "/Users/udit/git/btp/object-detector/ballTracking.py"
        # print "Calling: {} {} -v {} -a {} -s {}".format(python_bin, script_path, filename[0], self.action_flag, self.slide_flag)
        # subprocess.call(["open", "-a", "Terminal", python_bin, script_path, "-v", filename[0], "-a", self.action_flag, "-s", self.slide_flag])
        # Write arguments in text file
        file = open("args.txt", "w")
        file.write("{} {} -v {} -a {} -s {}".format(python_bin, script_path, filename[0], self.action_flag, self.slide_flag))
        file.close()
        subprocess.call(["open", "-a", "Terminal", "./analyze.sh"])

    # Run 3d.py
    def visualize(self, *args):
        script_path = "/Users/udit/git/btp/object-detector/3d.py"
        python_bin = "python"
        file = open("args.txt", "w")
        file.write("{} {} -v {}".format(python_bin, script_path, self.vflag))
        file.close()
        subprocess.call(["open", "-a", "Terminal", "./visualize.sh"])
        # subprocess.Popen([python_bin, script_path])
        # os.system("python "+script_path)
        # os.fork()
        # os.execl("/Users/udit/.virtualenvs/cv/bin/python", script_path)

# Create the screen manager and add all screens to it
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))

class BTP(App):
    def build(self):
        return sm

if __name__ == '__main__':
    BTP().run()