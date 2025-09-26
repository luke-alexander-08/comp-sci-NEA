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
        self.screen = screen
        self.values_dict = {}
        self.x = x
        self.y = y
    
    def add_slider(self, screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key):
        self.sliders.append(LabeledSlider(screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key=key, label_fontsize=15))

    def add_button(self, screen, x, y, width, height, text, passed_func):
        params = self.values_dict.values()
        self.buttons.append(Button(screen, x, y, width, height, text=text, onClick=passed_func))  

    def on_button_click(self):
        print("Clicked!")
    
    def get_params(self):
        return self.values_dict

    def update(self):
        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update() # store slider values in self dictionary. uses key identifier


