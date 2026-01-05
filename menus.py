from perlinNoise import perlin
import matplotlib.pyplot as plt
import pygame
from slider import LabeledSlider
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.dropdown import Dropdown
import numpy as np
import os
import json

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

    def add_slider(self, screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key, initial, handleRadius=None):
        temp = LabeledSlider(screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key=key, label_fontsize=15, initial=initial, handleRadius=handleRadius)
        self.sliders.append(temp)
        self.widgets.append(temp)

    def add_button(self, screen, x, y, width, height, text, passed_func, hidden=False, independent = False):
        temp = Button(screen, x, y, width, height, text=text, onClick=passed_func)
        if hidden:
            temp.hide()
        if not independent:
            self.buttons.append(temp)  
            self.widgets.append(temp)
        
        return temp

    def add_textbox(self, screen, x, y, width, height, fontsize, text="", disabled=True, hidden=False, independent= False, colour=(220,220,220), borderThickness=3, on_submit = lambda: print(), setText = None):
        temp = TextBox(screen, x, y, width, height, fontSize=fontsize, placeholderText = text, onSubmit=on_submit, colour = colour, borderThickness=borderThickness, )
        # if disabled:
        if disabled:
            temp.disable()
        if hidden:
            temp.hide()
        if not independent:
            self.widgets.append(temp)
        if setText is not None:
            temp.setText(setText)
        
        return temp

    def get_params(self):
        return self.values_dict

    def update(self):
        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update() # store slider values in self dictionary. uses key identifier

    def on_open(self):
        print(f"Now showing {self.ID} screen")

    def show_self(self):
        for widget in self.widgets:
            if widget.isEnabled():
                widget.enable()
            widget.show()
        
    def hide_self(self):
        for widget in self.widgets:
            # widget.disable()
            widget.hide()

    def get_ID(self):
        return self.ID
    
    def update_dict(self, key, value):
        self.values_dict[key] = value
        print(self.values_dict)

class GenerationMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, MENU_WIDTH, screen_change, back_screen, gen_map):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "GENERATION"

        self.add_textbox(screen=screen, x=20, y=0, height=25, width=256, fontsize=20, text="Altitude Parameters")
        self.add_slider(screen=screen, x=20, y=60, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="altitude_octaves", initial=8)
        self.add_slider(screen=screen, x=20, y=160, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=32, slider_step=0.01, label_text="Frequency", key="altitude_frequency", initial=2)
        self.add_slider(screen=screen, x=20, y=260, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="altitude_amplitude", initial=2)
        self.add_slider(screen=screen, x=20, y=360, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.01, label_text="Persistence", key="altitude_persistence", initial=0.5)
        self.add_slider(screen=screen, x=20, y=460, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.01, label_text="Lacunarity", key="altitude_lacunarity", initial=2.0)
        
        self.add_textbox(screen=screen, x=296, y=0, height=25, width=256, fontsize=20, text="Moisture Parameters")
        self.add_slider(screen=screen, x=296, y=60, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="moisture_octaves", initial=8)
        self.add_slider(screen=screen, x=296, y=160, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=32, slider_step=0.25, label_text="Frequency", key="moisture_frequency", initial=2)
        self.add_slider(screen=screen, x=296, y=260, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="moisture_amplitude", initial=2)
        self.add_slider(screen=screen, x=296, y=360, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.01, label_text="Persistence", key="moisture_persistence", initial=0.5)
        self.add_slider(screen=screen, x=296, y=460, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.01, label_text="Lacunarity", key="moisture_lacunarity", initial=2.0)

        self.add_textbox(screen=screen, x=572, y=0, height=25, width=256, fontsize=20, text="Temperature Parameters")
        self.add_slider(screen=screen, x=572, y=60, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=16, slider_step=1, label_text="Octaves", key="temperature_octaves", initial=8)
        self.add_slider(screen=screen, x=572, y=160, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=32, slider_step=0.001, label_text="Frequency", key="temperature_frequency", initial=2)
        self.add_slider(screen=screen, x=572, y=260, slider_width=MENU_WIDTH, slider_height=15, slider_min=1, slider_max=32, slider_step=0.25, label_text="Amplitude", key="temperature_amplitude", initial=2)
        self.add_slider(screen=screen, x=572, y=360, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=2, slider_step=0.01, label_text="Persistence", key="temperature_persistence", initial=0.5)
        self.add_slider(screen=screen, x=572, y=460, slider_width=MENU_WIDTH, slider_height=15, slider_min=0, slider_max=4, slider_step=0.01, label_text="Lacunarity", key="temperature_lacunarity", initial=2.0)
       
        self.seed_box = self.add_textbox(screen=screen, x=150, y=650, width=100, height=40, fontsize=15, setText="0", disabled=False)
        self.width_box = self.add_textbox(screen=screen, x=150, y=700, width=100, height=40, fontsize=15, setText="1024", disabled=False)
        self.height_box = self.add_textbox(screen=screen, x=150, y=750, width=100, height=40, fontsize=15, setText="512", disabled=False)
   
        self.add_textbox(screen=screen, x=0, y=650, width=150, height=40, fontsize=15, text="Generation Seed:")
        self.add_textbox(screen=screen, x=0, y=700, width=150, height=40, fontsize=15, text="Map Width:")
        self.add_textbox(screen=screen, x=0, y=750, width=150, height=40, fontsize=15, text="Map Height:")

        # self.add_textbox(screen=screen, x=150, y=650, width=100, height=40, fontsize=15, text="0", disabled=False, on_submit=lambda: self.update_dict("SEED"))

        self.add_button(screen=screen, x=296, y=530, width = 100, height = 30, text= "Generate", passed_func=lambda: (self.get_txtbox_values(), screen_change("LOAD"), gen_map(self.get_params()))) # add gen map functions to lambda function later
        self.add_button(screen=screen, x=screen_width-100, y=50, width = 100, height = 30, text= "Help", passed_func=lambda: (screen_change("HELP"))) # add gen map functions to lambda function later

    def get_txtbox_values(self):
        self.update_dict("SEED", int(self.seed_box.getText())) # initialise noise values
        self.update_dict("perlin_width", int(self.width_box.getText()))
        self.update_dict("perlin_height", int(self.height_box.getText()))

class WelcomeMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "WELCOME"

        self.add_textbox(screen=screen, x= 250, y=50, width=0, height = 75, fontsize=50, text="Map Generation Program", colour=(255,255,255), borderThickness=0)
        self.add_button(screen=screen, x= 312, y= 150, height=30, width=200, text="Import Menu", passed_func=lambda: screen_change("IMPORT"))
        self.add_button(screen=screen, x= 568, y= 150, height=30, width=200, text="Generation Menu", passed_func=lambda: screen_change("GENERATION"))

class ImportMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen, import_map):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "IMPORT"
        self.import_func = import_map
        self.import_box = self.add_textbox(screen=screen, x=100, y=100, height=100, width=200, fontsize=50, text="Enter file name: ", disabled=False, on_submit=self.callback)
        self.add_button(screen=screen, x= 50, y= 100, height=30, width=100, text="load", passed_func=lambda: self.callback())
        # self.add_button(screen=screen, x= 100, y=150, width=200, height=50, text="Import", passed_func=lambda: print("button"))

    def callback(self):
        self.import_func(self.import_box.getText())
        
    def on_open(self):
        print(f"Now showing {self.ID} screen")
        self.import_box.setText("")

class HelpMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "HELP"
        self.help_menu_text = [
"This menu is to provide some guidance on how each parameter on the generation menu changes the resulting noise generated.",
"I would recommend using this menu as a starting point and then messing around with the values to observe how the map changes. ",
"Octaves - Defines how many layers of noise are generated. Layers are summed and help create smaller details on biome edges. ",
"Frequency - Defines how zoomed in the map appears. A higher frequency is more zoomed out. ",
"Amplitude - Multiplies the significance of each layer, so that higher values of noise are more common. ",
"Persistence - Defines how much each layer is diminished by each iteration. ",
"Lacunarity - Defines what frequency of map is sampled each iteration. Changes how \"fuzzy\" the map looks. ",
        ]

        for number, line in enumerate(self.help_menu_text):
            self.add_textbox(screen=screen, x=100, y=60*number, height=50, width=screen_width-200, fontsize=15, text=line, disabled=False, colour = (255,255,255), borderThickness=0)
        


class LoadingMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen, get_perlin_progress):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "LOAD"
        self.get_perlin_progress = get_perlin_progress
        self.perlin_progress_bar = ProgressBar(self.screen, self.screen_width/2-100, self.screen_height/2, 500, 50, self.get_perlin_progress)
        self.perlin_progress_bar.hide()
        self.widgets.append(self.perlin_progress_bar)
        self.bar_text = self.add_textbox(self.screen, self.screen_width/2, (self.screen_height/2)-200, 300, 50, 30, "")

    def setloadingtext(self, text):
        self.bar_text.setText(text)

class MapMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen, perlin_map, perlin_width, perlin_height, view_libs):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "MAP"

        self.map_size = (perlin_width, perlin_height)
        self.new_map_dims = self.map_size
        self.perlin_map = perlin_map
        self.map_surf = pygame.Surface((perlin_width, perlin_height)) #
        self.scaled_surf = self.map_surf.copy()

        self.add_button(screen=screen, x= screen_width-50, y= 100, height=30, width=100, text="view libs", passed_func=view_libs)
        self.add_button(screen=screen, x= screen_width-50, y= 200, height=30, width=100, text="save", passed_func=self.toggle_save_box)

        self.save_box = self.add_textbox(screen=screen, x=250, y=550, height=100, width=200, fontsize=50, text="Enter file name: ", disabled=False, hidden=True, independent=True)
        self.save_button = self.add_button(screen=screen, x= 450, y= 550, height=100, width=100, text="save", passed_func=self.save_map, hidden=True, independent = True)
     
        self.mouse_pos_before_zoom = pygame.Vector2()
        self.zoom_scale = 1

        self.pan_offset = pygame.Vector2() # pygame object for handling vectors
        self.panned_map_coords = ((0,0) - self.pan_offset) * self.zoom_scale

        self.add_button(screen=screen, x= screen_width-50, y= 250, height=30, width=100, text="edit menu", passed_func=self.open_edit_menu)

        #edit menu
        self.edit_menu = EditMenu(screen, 0, 0, screen_width=screen_width, screen_height=screen_height, screen_change=screen_change, back_screen=back_screen, perlin_width=perlin_width, perlin_height=perlin_height, conv_screen_to_map_coords=self.conv_screen_to_map_coords, conv_map_to_screen_coords=self.conv_map_to_screen_coords)

    def set_map_size(self, width, height):
        self.map_surf = pygame.Surface((width, height)) 
        self.map_size = (width, height) # delete line for auto-centre on small maps. 

    def conv_screen_to_map_coords(self, coord):
        return int((coord[0]-self.pan_offset[0])*self.zoom_scale), int((coord[1]-self.pan_offset[1])*self.zoom_scale)

    def conv_map_to_screen_coords(self, coord):
        print((coord[0]-self.pan_offset[0])*self.zoom_scale), int((coord[1]-self.pan_offset[1]))
        print(coord, "coord")
        return int((coord[0]/self.zoom_scale) + self.pan_offset[0]), int((coord[1]/self.zoom_scale) + self.pan_offset[1])


    def set_map(self, map, imported=False): # discuss when writing up import function. 
        self.perlin_map = map
        if not imported:
            self.perlin_map = self.perlin_map.transpose(1,0,2)
        
        pygame.surfarray.blit_array(self.map_surf, self.perlin_map)
        self.scaled_surf = self.map_surf.copy()
        
    #override
    def update(self):
        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update()

       # render map on screen. 

        # print(self.perlin_map.shape)
        # print(self.map_surf.get_size())
        pygame.surfarray.blit_array(self.map_surf, self.perlin_map)
        self.panned_map_coords = ((0,0) - self.pan_offset) * self.zoom_scale
        # print(self.panned_map_coords)
        self.screen.blit(self.scaled_surf,self.panned_map_coords)

        self.edit_menu.update()

    def set_pan(self, pan_offset):
        self.pan_offset -= pan_offset/self.zoom_scale
        self.edit_menu.pan_offset = self.pan_offset
    
    def zoom_map(self, mouse_pos, direction):
        mouse_pos_before_zoom = pygame.Vector2(mouse_pos) / self.zoom_scale + self.pan_offset # finds the "world position" of mouse before any zooming.

        if direction == "IN":
            self.zoom_scale *= 1.05 # zoom in/out by 10%
        elif direction == "OUT":
            self.zoom_scale *= 0.95

        # potentialy limit extent of possible zoom. 

        map_dims = pygame.Vector2(self.map_size)
        new_map_dims = map_dims * self.zoom_scale
        self.scaled_surf = pygame.transform.scale(self.map_surf, new_map_dims)
        # now using old world pos can adjust so the zoomed in map is offset to the mouse position. 
        self.pan_offset = mouse_pos_before_zoom - (pygame.Vector2(mouse_pos) / self.zoom_scale)
        self.edit_menu.zoom_canvas(self.pan_offset, new_map_dims, self.zoom_scale)


    def toggle_save_box(self):
        if self.save_box.isVisible():
            self.save_box.hide()
            self.save_button.hide()

        else:
            self.save_box.show()
            self.save_button.show()

    def save_map(self):
        print(self.perlin_map.shape)
        name = self.save_box.getText()
        
        structure_data = []
        for surface, info in self.edit_menu.surface_positions.items():
            if info["is_text"]:
                surface_name = "label"
            else:
                surface_name = self.edit_menu.get_structure_id(surface)
            print(surface_name)
            structure_data.append({"name": surface_name,"info": info})
            
        json_name = "json_" + name
        with open(f".\maps\{json_name}.json", "w") as f: 
            json.dump(structure_data, f, indent=4)

        np.save(f".\maps\{name}.npy", self.perlin_map)
        pygame.image.save(self.edit_menu.canvas, f".\maps\canvas_{name}.png")
        self.save_box.setText("")
        self.save_box.hide()
        self.save_button.hide()

    def open_edit_menu(self):
        self.edit_menu.toggle_active()

    def get_is_placing(self):
        return self.edit_menu.is_placing()

    def stop_placing(self):
        self.edit_menu.stop_placing()

    def set_edit_canvas(self, surf):
        self.edit_menu.set_canvas(surf)

    def on_open(self):
        print(f"Now showing {self.ID} screen")
        self.edit_menu.update_canvas()
    
    def import_edit_structure(self, info):
        self.edit_menu.import_structure(info)

class EditMenu(Menu):
    def __init__(self, screen, x, y, screen_width, screen_height, screen_change, back_screen, perlin_width, perlin_height, conv_screen_to_map_coords, conv_map_to_screen_coords):
        super().__init__(screen, x, y, screen_width, screen_height, screen_change, back_screen)
        self.ID = "EDIT"

        self.conv_screen_to_map_coords, self.conv_map_to_screen_coords = conv_screen_to_map_coords, conv_map_to_screen_coords
        # map to screen for storage, screen to map for display
        self.canvas = pygame.Surface((perlin_width, perlin_height), pygame.SRCALPHA)
        self.canvas.fill((0,0,0,0)) # makes it transparent
        self.scaled_canvas = self.canvas.copy()
        self.new_map_dims = (perlin_width, perlin_height)
        self.update_canvas()

        self.surface_positions = {} # store labels and their coordinates
        self.structures = {}
        self.load_structures()
        self.structure_dropdown = Dropdown(screen, 0, 200, 100, 30, name="Select Structure", choices=list(self.structures.keys()), values = list(self.structures.keys()))
        self.widgets.append(self.structure_dropdown)
        print(self.structures)

        self.add_textbox(screen, 0, 30, 100, 30, 15, text="EDIT MENU", hidden=True)
        self.add_button(screen=screen, x= 0, y= 50, height=30, width=100, text="Add Label", passed_func=self.add_label)
        self.add_button(screen=screen, x= 0, y= 150, height=30, width=100, text="Add Structure", passed_func=self.add_structure)
        self.add_button(screen=screen, x= 0, y= 250, height=30, width=100, text="Paint Map", passed_func=self.paint_map)
        # self.add_button(screen=screen, x= 0, y= 250, height=30, width=100, text="Carve Map", passed_func=self.add_geographical_effect)

        self.active = False
        self.placing_label = False
        self.placing_structure = False
        self.painting = False
        self.draw = False

        self.font = pygame.font.SysFont("Times New Roman", 15)

        self.add_slider(screen, 200, 500, 100, 20, 0, 255, 1, "Red", key="red",initial=0) 
        self.add_slider(screen, 200, 600, 100, 20, 0, 255, 1, "Blue", key="blue",initial=0)
        self.add_slider(screen, 200, 700, 100, 20, 0, 255, 1, "Green", key="green",initial=0)
        self.add_slider(screen, 350, 500, 100, 20, 1, 25, 1, "Brush Width", key="width",initial=3)

        self.paint_colour = (0,0,0)

        self.hide_self()

        self.last_pos = None

        self.zoom_scale = 1
        self.pan_offset = pygame.Vector2()

    def toggle_active(self):
        if self.active:
            self.active = False
            self.hide_self()
        else:
            self.show_self()
            [slider.hide() for slider in self.sliders]
            self.active = True

    def update(self):

        for obj in self.sliders:
            self.values_dict[obj.key] = obj.update() # store slider values in self dictionary. uses key identifier

        for label, dest in self.surface_positions.items():
            dest = dest["pos"]
            label_size = label.get_size()
            scale = pygame.Vector2(label_size) *self.zoom_scale
            scaled_label = pygame.transform.scale(label,scale)
            pygame.Surface.blit(self.screen, scaled_label, self.conv_screen_to_map_coords(dest))

        if self.placing_label:
            pygame.Surface.blit(self.screen, self.label, self.conv_screen_to_map_coords(((pygame.mouse.get_pos()[0])+5,(pygame.mouse.get_pos()[1])-5))) # loading
            print(self.surface_positions[self.label]["pos"], "key")
            self.surface_positions[self.label]["pos"] = self.conv_map_to_screen_coords(((pygame.mouse.get_pos()[0])+5, (pygame.mouse.get_pos()[1])-5)) # saving

        if self.placing_structure:
            pygame.Surface.blit(self.screen, self.structure, self.conv_screen_to_map_coords(((pygame.mouse.get_pos()[0])+5,(pygame.mouse.get_pos()[1])-5)))
            print(self.surface_positions[self.structure]["pos"], "key")
            self.surface_positions[self.structure]["pos"] = self.conv_map_to_screen_coords(((pygame.mouse.get_pos()[0])+5, (pygame.mouse.get_pos()[1])-5))

        if self.painting:
            self.paint_colour = (self.values_dict["red"], self.values_dict["green"], self.values_dict["blue"]) # set colour to sliders

            if self.draw:
                current_pos = self.conv_map_to_screen_coords(pygame.mouse.get_pos())

                if self.last_pos != None:
                    pygame.draw.line(self.canvas, self.paint_colour, (self.last_pos), (current_pos), width = self.values_dict["width"])
                    self.update_canvas()
                self.last_pos = (current_pos)
            else:
                self.last_pos = None

        self.panned_map_coords = ((0,0) - self.pan_offset) * self.zoom_scale
        self.screen.blit(self.scaled_canvas, self.panned_map_coords)

    def load_structures(self):
        for filename in os.listdir(".\structures"):
            if filename.endswith(".png"):
                filepath = os.path.join(".\structures", filename)
                image = pygame.image.load(filepath).convert_alpha() 
                image = pygame.transform.scale(image, (50,50))

                self.structures[filename.split(".")[0]] = image

    def get_structure_id(self, structure):
        for name, surf in self.structures.items():
            # direct object equality (same object)
            if surf == structure:
                return name
            if pygame.image.tostring(surf, 'RGBA') == pygame.image.tostring(structure, 'RGBA'): # compare pixels directly... not great
                return name
            
        
        return "label_structure"
    
    def add_label(self):
        self.label_box = self.add_textbox(self.screen, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 200, 30, 15, "Enter label name", disabled=False, on_submit=self.place_label, borderThickness=0, colour=(220,0,0,120))

    def place_label(self):
        self.label = self.font.render(self.label_box.getText(), 1, (0,0,0))
        self.surface_positions[self.label] = {"pos":(0,0), "is_text":True, "text":self.label_box.getText()}
        self.label_box.hide()
        self.placing_label = True

    def add_structure(self): # village, city, 
        print("Structure")
        self.structure = self.structures[self.structure_dropdown.getSelected()].copy()
        self.surface_positions[self.structure] = {"pos":pygame.Vector2(), "is_text":False, "text":None}
        self.placing_structure = True

    def import_structure(self, info):
        print(info, "info")
        if info["info"]["is_text"]:
            self.label = self.font.render(self.label_box.getText(), 1, (0,0,0))
            self.surface_positions[self.label] = info["info"]
        else:
            structure_surf = self.structures[info["name"]].copy()
            self.surface_positions[structure_surf] = info["info"]

    def add_geographical_effect(self, geo=""):
        print("Geography")

    def paint_map(self):
        if self.painting:
            [slider.hide() for slider in self.sliders]
            self.painting = False
            self.draw = False
        else:
            [slider.show() for slider in self.sliders]
            self.painting = True

    
    def is_placing(self):
        return (self.placing_label or self.placing_structure)
    
    def stop_placing(self):
        self.placing_label = False
        self.placing_structure = False
    
    def zoom_canvas(self, pan_offset, new_map_dims, zoom):
        print("Updated edit, ", pan_offset, zoom, new_map_dims)
        self.scaled_canvas = pygame.transform.scale(self.canvas, new_map_dims)
        self.new_map_dims = new_map_dims
        self.pan_offset = pan_offset
        self.zoom_scale = zoom

    def update_canvas(self):
        self.scaled_canvas = pygame.transform.scale(self.canvas, self.new_map_dims)

    def set_canvas(self, surf):
        self.canvas = surf