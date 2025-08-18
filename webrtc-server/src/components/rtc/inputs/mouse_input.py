from components.controllers.mouse_controller import MouseController

class MouseInput:
    def __init__(self):
        self.controller = MouseController()

    # event = [0, 1, 2, 3, 4]
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

        if (event == 0):  # Move
            position = eval(info[0])
            self.controller.move_to(position[0], position[1])
        elif (event == 1):  # Down
            self.controller.down(buttons[button])
        elif (event == 2):  # Release
            self.controller.up(buttons[button])
        elif (event == 3):  # Drag (a combination of move and a held-down button)
            position = eval(info[0])
            self.controller.move_to(position[0], position[1])
            # The 'down' state is implicitly handled by a prior 'down' event.
        elif (event == 4): # Scroll
            scroll_info = eval(info[0])
            # Scroll direction can be encoded as positive/negative values.
            self.controller.scroll(scroll_info)

    def parse_input(self, data):
        #Parses a string formatted as "event_type:event_code#info1:info2"
        try:
            event_info, *rest_of_info = data.split("#")
            
            event_parts = event_info.split(":")
            event_type = int(event_parts[1])
            button_code = int(event_parts[2])
            
            info = rest_of_info[0].split(":") if rest_of_info else []
            return event_type, button_code, info
        except (ValueError, IndexError) as e:
            print(f"Error parsing input data: {data}. Exception: {e}")
            return None, None, None
