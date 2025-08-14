class MouseInput:
    def __init__(self, on_input):
        self.on_input = on_input 

    # event = [0, 1, 2, 3]
    # 0=Move, 1=Down, 2=Release, 3=Drag, 4=Scroll

    # button = [0, 1, 2]
    # 0=Left, 1=Right, 2=Middle

    def input(self, event, button, info):
        data = {}
       
        # input type - mouse
        data["t"] = "m"
        data["e"] = event
        data["b"] = button
        data["i"] = info

        self.on_input(data)

    def move(self, position):
        info = {
            "p": position
        }
        self.input(0, 0, info)

    def down(self, button, position):
        info = {
            "p": position
        }
        self.input(1, button, info)

    def release(self, button, position):
        info = {
            "p": position
        }
        self.input(2, button, info)

    def drag(self, button, position, delta_position):
        info = {
            "p": position,
            "dp": delta_position
        }
        self.input(3, button, info)

    def scroll(self, button, value):
        info = {
            "v": value,
        }
        self.input(4, button, info)
