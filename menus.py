from perlinNoise import perlin
import matplotlib.pyplot as plt
import pygame
from slider import LabeledSlider
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button




class Menu():
    def __init__(self, screen, x, y):
        self.sliders = []
        self.buttons = []
        self.widgets = []

        self.screen = screen
        self.values_dict = {}
        self.x = x
        self.y = y
    
    def add_slider(self, screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key):
        temp = LabeledSlider(screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key=key, label_fontsize=15)
        self.sliders.append(temp)
        self.widgets.append(temp)

    def add_button(self, screen, x, y, width, height, text, passed_func):
        temp = Button(screen, x, y, width, height, text=text, onClick=passed_func)
        self.buttons.append(temp)  
        self.widgets.append(temp)

    def get_params(self):
        return self.values_dict

    def update(self):
        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update() # store slider values in self dictionary. uses key identifier

    def show_self(self):
        for widget in self.widgets:
            widget.enable()
            widget.show()
        
    def hide_self(self):
        for widget in self.widgets:
            widget.disable()
            widget.hide()


class GenerationMenu(Menu):
    def __init__(self, screen, x, y, MENU_WIDTH, screen_change):
        super().__init__(screen, x, y)
        self.add_slider(screen=screen, x=550, y=30, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="octaves")
        self.add_slider(screen=screen, x=550, y=130, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Frequency", key="frequency")
        self.add_slider(screen=screen, x=550, y=230, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="amplitude")
        self.add_slider(screen=screen, x=550, y=330, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.25, label_text="Persistence", key="persistence")
        self.add_slider(screen=screen, x=550, y=430, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.5, label_text="Lacunarity", key="lacunarity")
        self.add_slider(screen=screen, x=20, y=550, slider_width=100, slider_height=15, slider_min=-1.0, slider_max=1, slider_step=0.01, label_text="Blue Noise Boundary", key="blue_boundary")
        self.add_slider(screen=screen, x=20, y=650, slider_width=100, slider_height=15, slider_min=-1.0, slider_max=1, slider_step=0.01, label_text="Green Noise Boundary", key="green_boundary")
      
        self.add_button(screen=screen, x=550, y=530, width = 100, height = 30, text= "Generate", passed_func=lambda: screen_change("")) # add gen map functions to lambda function later

class WelcomeMenu(Menu):
    def __init__(self, screen, x, y, screen_change):
        super().__init__(screen, x, y)
        self.add_button(screen=screen, x= 50, y= 100, height=30, width=100, text="import", passed_func=lambda: screen_change("IMPORT"))
        self.add_button(screen=screen, x= 200, y= 100, height=30, width=100, text="generation", passed_func=lambda: screen_change("GENERATION"))

class ImportMenu(Menu):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)

class HelpMenu(Menu):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)

class MapMenu(Menu):
    def __init__(self, screen, x, y):
        super().__init__(screen, x, y)

