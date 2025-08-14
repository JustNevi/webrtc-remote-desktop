import json
import time
import threading

from components.rtc.inputs.mouse_input import MouseInput 
from components.rtc.inputs.keyboard_input import KeyboardInput 

class Input:
    def __init__(self, control_queue):
        self.mouse = MouseInput() 
        self.keyboard = KeyboardInput() 

        self.running = True
        self.control_queue = control_queue

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        while (self.running):
            processed = False 
            while (not self.control_queue.empty()):
                control = self.control_queue.get_nowait()
                self.control(control)
                processed = True
                time.sleep(0.05)
            if not processed:
                time.sleep(0.005)

    def control(self, message):
        js = json.loads(message)  

        ctype = self.parse_type(js)

        if (ctype == "m"):
            if (self.mouse):
                self.mouse.input(js)
        elif (ctype == "k"):
            if (self.keyboard):
                pass

    def parse_type(self, data):
        return data["t"]
