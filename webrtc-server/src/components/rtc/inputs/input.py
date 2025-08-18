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
                # Get control event message
                control = self.control_queue.get_nowait()
                # Control
                self.control(control)

                processed = True
            if not processed:
                time.sleep(0.0005)

    def control(self, message):
        ctype = self.parse_type(message)

        if (ctype == "m"):
            if (self.mouse):
                self.mouse.input(message)
        elif (ctype == "k"):
            if (self.keyboard):
                self.keyboard.input(message) 

    def parse_type(self, data):
        return data.split(":")[0]
