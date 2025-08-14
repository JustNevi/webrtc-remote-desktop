import json

class Input:
    def __init__(self, mouse_input=None, keyboard_input=None):
        self.mouse = mouse_input
        self.keyboard = keyboard_input 

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
