from components.rtc.inputs.mouse_input import MouseInput 
from components.rtc.inputs.keyboard_input import KeyboardInput 

class Input:
    def __init__(self, on_input):
        self.mouse = MouseInput(on_input) 
        self.keyboard = KeyboardInput(on_input) 
