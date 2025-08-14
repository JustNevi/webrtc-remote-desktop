import pyautogui as gui

class MouseController:
    def __init__(self):
        self.is_left_down = False
        self.is_right_down = False

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

    def up(self, button, x, y):
        if (button == "left"):
            self.is_left_down = False 
        elif (button == "right"):
            self.is_right_down = False 

        gui.mouseUp(x=x, y=y, button=button)
