import pyautogui as gui

class MouseController:
    def __init__(self):
        self.is_left_down = False
        self.is_right_down = False

        x, y = gui.size()
        self.size = (x, y) 

    def in_gui(func):
        def wrapper(self, button, x, y, *args, **kwargs):
            xg = x >=0 and x < self.size[0]
            yg = y >= 0 and y < self.size[1]
            if (xg and yg):
                func(self, button, x, y, *args, **kwargs)

        return wrapper

    @in_gui
    def down(self, button, x, y):
        if (button == "left"):
            if (self.is_left_down):
                return
            self.is_left_down = True
        elif (button == "right"):
            if (self.is_right_down):
                return
            self.is_right_down = True

        gui.mouseDown(x=x, y=y, button=button)

    @in_gui
    def up(self, button, x, y):
        if (button == "left"):
            self.is_left_down = False 
        elif (button == "right"):
            self.is_right_down = False 

        gui.mouseUp(x=x, y=y, button=button)
