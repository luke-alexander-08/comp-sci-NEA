import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# pygame.init()
# win = pygame.display.set_mode((1000, 600))

alphabet = []
numbers= ["1","2", "3", "4", "5", "6", "7", "8", "9"]

def is_valid_slider(val): # no negatives, no letters
    stripped_val = val.strip(".")

    if stripped_val.isnumeric() and int(stripped_val) >= 0:
        return True

    return False

class LabeledSlider():
    def __init__(self, screen, x, y, slider_width, slider_height, slider_min, slider_max, slider_step, label_text, key, label_fontsize=30, initial=0, handleRadius=None):
        if handleRadius is None:
            handleRadius = int(slider_height/1.3)
        
        print(initial, "intiial")
        
        self.slider = Slider(screen, x, y, slider_width, slider_height, min=slider_min, max=slider_max, step=slider_step, initial=initial, handleRadius=handleRadius)
        self.label = TextBox(screen, x, y-label_fontsize*2, 100, label_fontsize+10, fontSize=label_fontsize, borderThickness=0, colour=(255,255,255)) # postition the label above the slider
        self.label_text = label_text
        self.value_box = TextBox(screen, x, y+label_fontsize*2, slider_width, label_fontsize+20, fontSize=label_fontsize, borderThickness=1, onSubmit=self.on_text_submit)
        self.label.setText(label_text)
        self.label.disable()
        self.key=key

    def on_text_submit(self):
        print("Called")
        val = self.value_box.getText()
        is_valid = is_valid_slider(val)
        if is_valid:
            self.slider.setValue(float(val))
        else:
            print("Invalid Value! ")
    def hide(self):
        self.slider.hide()
        self.label.hide()
        self.value_box.hide()

    def show(self):
        self.slider.show()
        self.label.show()
        self.value_box.show()

    def enable(self):
        self.slider.enable()
        self.value_box.enable()
        # print("Enabled")

    def disable(self):
        self.slider.disable()
        self.value_box.disable()

    def update(self):
        if not self.value_box.selected: # allows for discrete value selection
            self.value_box.setText(str(round(self.slider.getValue(), 2)))  
            # print("slider update. ")
        
        return self.slider.getValue()

    def isEnabled(self):
        return self.label.isEnabled()






# slider_var= 15

# labelledslide = LabeledSlider(win, 100,500,800,40,0,99,1,"test")
# slider = Slider(win, 100, 100, 800, 40, min=0, max=99, step=1)
# output = TextBox(win, 475, 200, 100, 50, fontSize=30)

# output.disable()  # Act as label instead of textbox

# run = True
# while run:
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             run = False
#             quit()

#     win.fill((255, 255, 255))

#     output.setText(str(slider.getValue()))
#     slider_var = labelledslide.update()
     
#     pygame_widgets.update(events)
#     pygame.display.update()

#     print(slider_var)