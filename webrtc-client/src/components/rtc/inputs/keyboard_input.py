class KeyboardInput:
    def __init__(self, on_input):
        self.on_input = on_input 

    # event = [0, 1]
    # 0=Press, 1=Release

    def input(self, event, key):
        data = "" 
       
        # "k:" input type - keyboard
        data = f"k:{event}:{key}"

        self.on_input(data)

    def press(self, key):
        self.input(0, key)

    def release(self, key):
        self.input(1, key)
