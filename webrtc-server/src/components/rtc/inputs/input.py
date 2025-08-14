import json

from components.rtc.inputs.mouse_input import MouseInput 
from components.rtc.inputs.keyboard_input import KeyboardInput 

class Input:
    def __init__(self):
        self.mouse = MouseInput() 
        self.keyboard = KeyboardInput() 

    def on_message(self, message):
        js = json.loads(message)  

        ctype = self.parse_type(js)

        if (ctype == "m"):
            if (self.mouse):
                self.mouse.input(js)
        elif (ctype == "k"):
            if (self.keyboard):
                self.keyboard.input(js)

    def parse_type(self, data):
        return data["t"]
