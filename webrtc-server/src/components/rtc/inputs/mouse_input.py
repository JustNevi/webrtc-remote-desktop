class MouseInput:
    def __init__(self):
        pass

    # event = [0, 1, 2, 3]
    # 0=Down, 1=Release, 2=Drag, 3=Scroll

    # buttom = [0, 1, 2]
    # 0=Left, 1=Right, 2=Middle

    def input(self, data):
        event, button, info = self.parse_input(data) 

        self.on_input(data)

    def parse_input(self, data):
        return data["e"], data["b"], data["i"]

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

    def scroll(self, buttom, value):
        info = {
            "v": value,
        }
        self.input(3, buttom, info)
