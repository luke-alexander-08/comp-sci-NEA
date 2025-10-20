from perlinNoise import perlin
import matplotlib.pyplot as plt
import pygame
from slider import LabeledSlider
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button




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

    def add_slider(self, screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key):
        temp = LabeledSlider(screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key=key, label_fontsize=15)
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

        self.add_slider(screen=screen, x=550, y=30, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="octaves")
        self.add_slider(screen=screen, x=550, y=130, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Frequency", key="frequency")
        self.add_slider(screen=screen, x=550, y=230, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="amplitude")
        self.add_slider(screen=screen, x=550, y=330, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.25, label_text="Persistence", key="persistence")
        self.add_slider(screen=screen, x=550, y=430, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.5, label_text="Lacunarity", key="lacunarity")
        self.add_slider(screen=screen, x=20, y=550, slider_width=100, slider_height=15, slider_min=-1.0, slider_max=1, slider_step=0.01, label_text="Blue Noise Boundary", key="blue_boundary")
        self.add_slider(screen=screen, x=20, y=650, slider_width=100, slider_height=15, slider_min=-1.0, slider_max=1, slider_step=0.01, label_text="Green Noise Boundary", key="green_boundary")
      
        self.add_button(screen=screen, x=550, y=530, width = 100, height = 30, text= "Generate", passed_func=lambda: (screen_change("MAP"), gen_map(self.get_params()))) # add gen map functions to lambda function later

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
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen, perlin_map, perlin_width, perlin_height):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "MAP"

        # self.add_textbox(screen=screen, x=100, y=100, height=50, width=50, fontsize=50, text="GENERATION MENU!!!!")
        self.perlin_map = perlin_map
        self.map_surf = pygame.Surface((perlin_width, perlin_height)) #

    def set_map(self, map):
        self.perlin_map = map
    
    #override
    def update(self):
        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update()

       # render map on screen. 
        pygame.surfarray.blit_array(self.map_surf, self.perlin_map)
        self.screen.blit(self.map_surf,(0,0))

