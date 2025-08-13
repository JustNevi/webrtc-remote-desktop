class MouseInput:
    def __init__(self, on_input):
        self.on_input = on_input 

    # event = [0, 1, 2]
    # 0=Down, 1=Release, 2=Drag

    # buttom = [0, 1, 2]
    # 0=Left, 1=Right, 2=Middle

    def input(self, event, buttom, info):
        data = {}
       
        # input type - mouse
        data["t"] = "m"
        data["e"] = event
        data["b"] = buttom
        data["i"] = info

        self.on_input(data)

    def down(self, buttom, position):
        info = {
            "p": position
        }
        self.input(0, buttom, info)

    def release(self, buttom, position):
        info = {
            "p": position
        }
        self.input(1, buttom, info)

    def drag(self, buttom, position, delta_position):
        info = {
            "p": position,
            "dp": delta_position
        }
        self.input(2, buttom, info)
