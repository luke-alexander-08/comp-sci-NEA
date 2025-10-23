from perlinNoise import perlin
import matplotlib.pyplot as plt
import pygame
from slider import LabeledSlider
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import numpy as np



class Menu():
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen):
        self.ID = "Template"
        
        self.sliders = []
        self.buttons = []
        self.widgets = []

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.values_dict = {}
        self.x = x
        self.y = y

        #add home and back button to all screens
        self.add_button(screen, screen_width - 50, 20, 50, 20, "Home", lambda: screen_change("WELCOME"))        
        self.add_button(screen, screen_width - 50, 80, 50, 20, "Back", back_screen)        

    def add_slider(self, screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key, initial):
        temp = LabeledSlider(screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key=key, label_fontsize=15, initial=initial)
        self.sliders.append(temp)
        self.widgets.append(temp)

    def add_button(self, screen, x, y, width, height, text, passed_func):
        temp = Button(screen, x, y, width, height, text=text, onClick=passed_func)
        self.buttons.append(temp)  
        self.widgets.append(temp)

    def add_textbox(self, screen, x, y, width, height, fontsize, text):
        temp = TextBox(screen, x, y, width, height, fontSize=fontsize, placeholderText = text)
        temp.disable()
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

    def get_ID(self):
        return self.ID

class GenerationMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, MENU_WIDTH, screen_change, back_screen, gen_map):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "GENERATION"

        self.add_textbox(screen=screen, x=20, y=0, height=25, width=256, fontsize=20, text="Altitude Parameters")
        self.add_slider(screen=screen, x=20, y=60, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="altitude_octaves", initial=8)
        self.add_slider(screen=screen, x=20, y=160, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=32, slider_step=0.01, label_text="Frequency", key="altitude_frequency", initial=0.001)
        self.add_slider(screen=screen, x=20, y=260, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="altitude_amplitude", initial=2)
        self.add_slider(screen=screen, x=20, y=360, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.01, label_text="Persistence", key="altitude_persistence", initial=0.5)
        self.add_slider(screen=screen, x=20, y=460, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.01, label_text="Lacunarity", key="altitude_lacunarity", initial=2.0)
        
        self.add_textbox(screen=screen, x=296, y=0, height=25, width=256, fontsize=20, text="Moisture Parameters")
        self.add_slider(screen=screen, x=296, y=60, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="moisture_octaves", initial=8)
        self.add_slider(screen=screen, x=296, y=160, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=32, slider_step=0.25, label_text="Frequency", key="moisture_frequency", initial=0.001)
        self.add_slider(screen=screen, x=296, y=260, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="moisture_amplitude", initial=2)
        self.add_slider(screen=screen, x=296, y=360, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.01, label_text="Persistence", key="moisture_persistence", initial=0.5)
        self.add_slider(screen=screen, x=296, y=460, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.01, label_text="Lacunarity", key="moisture_lacunarity", initial=2.0)

        self.add_textbox(screen=screen, x=572, y=0, height=25, width=256, fontsize=20, text="Temperature Parameters")
        self.add_slider(screen=screen, x=572, y=60, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="temperature_octaves", initial=8)
        self.add_slider(screen=screen, x=572, y=160, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=32, slider_step=0.001, label_text="Frequency", key="temperature_frequency", initial=0.001)
        self.add_slider(screen=screen, x=572, y=260, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="temperature_amplitude", initial=2)
        self.add_slider(screen=screen, x=572, y=360, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.01, label_text="Persistence", key="temperature_persistence", initial=0.5)
        self.add_slider(screen=screen, x=572, y=460, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.01, label_text="Lacunarity", key="temperature_lacunarity", initial=2.0)


        self.add_button(screen=screen, x=296, y=530, width = 100, height = 30, text= "Generate", passed_func=lambda: (screen_change("MAP"), gen_map(self.get_params()))) # add gen map functions to lambda function later

class WelcomeMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "WELCOME"

        self.add_button(screen=screen, x= 50, y= 100, height=30, width=100, text="import", passed_func=lambda: screen_change("IMPORT"))
        self.add_button(screen=screen, x= 200, y= 100, height=30, width=100, text="generation", passed_func=lambda: screen_change("GENERATION"))

class ImportMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "IMPORT"

        self.add_textbox(screen=screen, x=100, y=100, height=50, width=50, fontsize=50, text="IMPORT MENU!!!!")

class HelpMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "HELP"


class MapMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen, perlin_map, perlin_width, perlin_height, view_libs):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "MAP"

        # self.add_textbox(screen=screen, x=100, y=100, height=50, width=50, fontsize=50, text="GENERATION MENU!!!!")
        self.perlin_map = perlin_map
        self.map_surf = pygame.Surface((perlin_width, perlin_height)) #

        self.add_button(screen=screen, x= screen_width-50, y= 100, height=30, width=100, text="view libs", passed_func=view_libs)
        self.add_button(screen=screen, x= screen_width-50, y= 200, height=30, width=100, text="save", passed_func=self.save_map)

    def set_map(self, map):
        self.perlin_map = map  
        self.perlin_map = self.perlin_map.transpose(1,0,2)
    
    #override
    def update(self):
        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update()

       # render map on screen. 
        pygame.surfarray.blit_array(self.map_surf, self.perlin_map)
        self.screen.blit(self.map_surf,(0,0))

    def save_map(self):
        name_temp = input("fileName: ")
        np.save(f".\{name_temp}", self.perlin_map)
