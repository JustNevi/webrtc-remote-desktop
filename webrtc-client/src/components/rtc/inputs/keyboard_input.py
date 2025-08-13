class KeyboardInput:
    def __init__(self, on_input):
        self.on_input = on_input 

    # event = [0, 1]
    # 0=Press, 1=Release

    def input(self, event, key):
        data = {}
       
        # input type - keyboard
        data["t"] = "k"
        data["e"] = event
        data["k"] = key 

        self.on_input(data)

    def press(self, key):
        self.input(0, key)

    def release(self, key):
        self.input(1, key)
