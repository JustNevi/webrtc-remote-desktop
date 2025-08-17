from components.controllers.keyboard_controller import KeyboardController

class KeyboardInput:
    def __init__(self):
        self.controller = KeyboardController()

    # event = [0, 1]
    # 0=Press, 1=Release

    def input(self, data):
        event, keyname = self.parse_input(data)

        if (event == 0): # Press
            self.controller.key_down(keyname)
        elif (event == 1): # Release 
            self.controller.key_up(keyname)
       

    def press(self, key):
        self.input(0, key)

    def release(self, key):
        self.input(1, key)

    def parse_input(self, data):
        #Parses a string formatted as "event_type:event_code:keyname"
        try:
            data_split = data.split(":")

            return int(data_split[1]), data_split[2]
        except (ValueError, IndexError) as e:
            print(f"Error parsing input data: {data}. Exception: {e}")
            return None, None, None
