from Xlib import display, X, XK
import Xlib.ext.xtest

class KeyboardController:
    def __init__(self):
        self.disp = display.Display()

    def _get_keysym(self, key_name):
        # Handle regular character keys
        return XK.string_to_keysym(key_name)

    def key_down(self, key_name):
        keysym = self._get_keysym(key_name)
        if keysym == X.NoSymbol:
            print(f"Warning: No keysym found for key '{key_name}'")
            return

        keycode = self.disp.keysym_to_keycode(keysym)
        if keycode == 0:
            print(f"Warning: No keycode found for keysym {keysym}")
            return
        Xlib.ext.xtest.fake_input(self.disp, X.KeyPress, keycode)
        self.disp.sync()

    def key_up(self, key_name):
        keysym = self._get_keysym(key_name)
        if keysym == X.NoSymbol:
            return

        keycode = self.disp.keysym_to_keycode(keysym)
        if keycode == 0:
            return
        
        Xlib.ext.xtest.fake_input(self.disp, X.KeyRelease, keycode)
        self.disp.sync()
