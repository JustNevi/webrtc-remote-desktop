from components.controllers.mouse_controller import MouseController

class MouseInput:
    def __init__(self):
        self.controller = MouseController() 

    # event = [0, 1, 2, 3]
    # 0=Move, 1=Down, 2=Release, 3=Drag, 4=Scroll

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
            position = eval(info[0])
            self.controller.move(buttons[button], position[0], position[1])
        elif (event == 1):
            position = eval(info[0])
            self.controller.down(buttons[button], position[0], position[1])
        elif (event == 2):
            position = eval(info[0])
            self.controller.up(buttons[button], position[0], position[1])

    def parse_input(self, data):
        event_info = data.split("#")

        event = event_info[0].split(":")
        info = event_info[1].split(":")
         
        return int(event[1]), int(event[2]), info
