from Xlib import display, X
from Xlib.ext.xtest import fake_input

class MouseController:
    def __init__(self):
        self.disp = display.Display()
    
    def move_to(self, x, y):
        fake_input(self.disp, X.MotionNotify, x=x, y=y)
        self.disp.sync()
    
    def _button_event(self, button, is_down):
        event_type = X.ButtonPress if is_down else X.ButtonRelease
        fake_input(self.disp, event_type, button)
        self.disp.flush()
    
    def down(self, button):
        button_map = {"left": 1, "right": 3, "middle": 2}
        if button in button_map:
            self._button_event(button_map[button], True)
    
    def up(self, button):
        button_map = {"left": 1, "right": 3, "middle": 2}
        if button in button_map:
            self._button_event(button_map[button], False)
    
    def click(self, button="left"):
        self.down(button)
        self.up(button)
    
    def scroll(self, direction):
        # Direction > 0 for scroll up, < 0 for scroll down.
        # 4 is scroll up, 5 is scroll down
        button = 4 if direction > 0 else 5  
        self._button_event(button, True)
        self.disp.sync()
        self._button_event(button, False)
        self.disp.sync()
    
    def get_screen_size(self):
        # Retrieves the screen size for reference.
        screen = self.disp.screen()
        return (screen.width_in_pixels, screen.height_in_pixels)
