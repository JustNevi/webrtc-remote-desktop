from components.controllers.mouse_controller import MouseController

class MouseInput:
    def __init__(self):
        self.controller = MouseController() 

    # event = [0, 1, 2, 3]
    # 0=Down, 1=Release, 2=Drag, 3=Scroll

    # button = [0, 1, 2]
    # 0=Left, 1=Right, 2=Middle

    def input(self, data):
        event, button, info = self.parse_input(data) 
        
        buttons = {
            0: "left",
            1: "right",
            2: "middle"
        }

        if (event == 0):
            position = info["p"]
            self.controller.down(buttons[button], position[0], position[1])
        elif (event == 1):
            position = info["p"]
            self.controller.up(buttons[button], position[0], position[1])

    def parse_input(self, data):
        return data["e"], data["b"], data["i"]
