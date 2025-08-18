import dearpygui.dearpygui as dpg

class KeyboardInput:
    def __init__(self, on_input):
        self.on_input = on_input 

    # event = [0, 1]
    # 0=Press, 1=Release

    def input(self, event, key):
        data = ""

        keyname = self.keycode_into_keyname(key)

        if (keyname):
            # "k:" input type - keyboard
            data = f"k:{event}:{keyname}"

            self.on_input(data)

    def press(self, key):
        self.input(0, key)

    def release(self, key):
        self.input(1, key)

    def keycode_into_keyname(self, keycode):
        map = {
            # Numbers
            dpg.mvKey_0: "0",
            dpg.mvKey_1: "1",
            dpg.mvKey_2: "2",
            dpg.mvKey_3: "3",
            dpg.mvKey_4: "4",
            dpg.mvKey_5: "5",
            dpg.mvKey_6: "6",
            dpg.mvKey_7: "7",
            dpg.mvKey_8: "8",
            dpg.mvKey_9: "9",
            # Letters
            dpg.mvKey_A: "a",
            dpg.mvKey_B: "b",
            dpg.mvKey_C: "c",
            dpg.mvKey_D: "d",
            dpg.mvKey_E: "e",
            dpg.mvKey_F: "f",
            dpg.mvKey_G: "g",
            dpg.mvKey_H: "h",
            dpg.mvKey_I: "i",
            dpg.mvKey_J: "j",
            dpg.mvKey_K: "k",
            dpg.mvKey_L: "l",
            dpg.mvKey_M: "m",
            dpg.mvKey_N: "n",
            dpg.mvKey_O: "o",
            dpg.mvKey_P: "p",
            dpg.mvKey_Q: "q",
            dpg.mvKey_R: "r",
            dpg.mvKey_S: "s",
            dpg.mvKey_T: "t",
            dpg.mvKey_U: "u",
            dpg.mvKey_V: "v",
            dpg.mvKey_W: "w",
            dpg.mvKey_X: "x",
            dpg.mvKey_Y: "y",
            dpg.mvKey_Z: "z",
            # Function Keys
            dpg.mvKey_F1: "F1",
            dpg.mvKey_F2: "F2",
            dpg.mvKey_F3: "F3",
            dpg.mvKey_F4: "F4",
            dpg.mvKey_F5: "F5",
            dpg.mvKey_F6: "F6",
            dpg.mvKey_F7: "F7",
            dpg.mvKey_F8: "F8",
            dpg.mvKey_F9: "F9",
            dpg.mvKey_F10: "F10",
            dpg.mvKey_F11: "F11",
            dpg.mvKey_F12: "F12",
            dpg.mvKey_F13: "F13",
            dpg.mvKey_F14: "F14",
            dpg.mvKey_F15: "F15",
            dpg.mvKey_F16: "F16",
            dpg.mvKey_F17: "F17",
            dpg.mvKey_F18: "F18",
            dpg.mvKey_F19: "F19",
            dpg.mvKey_F20: "F20",
            dpg.mvKey_F21: "F21",
            dpg.mvKey_F22: "F22",
            dpg.mvKey_F23: "F23",
            dpg.mvKey_F24: "F24",
            dpg.mvKey_F25: "F25",
            # Numpad Keys
            dpg.mvKey_NumPad0: "NumPad0",
            dpg.mvKey_NumPad1: "NumPad1",
            dpg.mvKey_NumPad2: "NumPad2",
            dpg.mvKey_NumPad3: "NumPad3",
            dpg.mvKey_NumPad4: "NumPad4",
            dpg.mvKey_NumPad5: "NumPad5",
            dpg.mvKey_NumPad6: "NumPad6",
            dpg.mvKey_NumPad7: "NumPad7",
            dpg.mvKey_NumPad8: "NumPad8",
            dpg.mvKey_NumPad9: "NumPad9",
            dpg.mvKey_NumPadEnter: "NumPadEnter",
            dpg.mvKey_NumPadEqual: "NumPadEqual",
            dpg.mvKey_Subtract: "Subtract",
            dpg.mvKey_Decimal: "Decimal",
            dpg.mvKey_Divide: "Divide",
            dpg.mvKey_Multiply: "Multiply",
            dpg.mvKey_Add: "Add",
            # Modifier & Special Keys
            dpg.mvKey_LShift: "Shift_L",
            dpg.mvKey_RShift: "Shift_R",
            dpg.mvKey_LControl: "Control_L",
            dpg.mvKey_RControl: "Control_R",
            dpg.mvKey_LAlt: "Alt_L",
            dpg.mvKey_RAlt: "Alt_R",
            dpg.mvKey_LWin: "LWin",
            dpg.mvKey_RWin: "RWin",
            dpg.mvKey_ModSuper: "ModSuper",
            dpg.mvKey_ModShift: "ModShift",
            dpg.mvKey_ModAlt: "ModAlt",
            dpg.mvKey_ModCtrl: "ModCtrl",
            # Navigation & Editing Keys
            dpg.mvKey_Back: "BackSpace",
            dpg.mvKey_Tab: "Tab",
            dpg.mvKey_Return: "Return",
            dpg.mvKey_Spacebar: "space",
            dpg.mvKey_End: "End",
            dpg.mvKey_Home: "Home",
            dpg.mvKey_Left: "Left",
            dpg.mvKey_Up: "Up",
            dpg.mvKey_Right: "Right",
            dpg.mvKey_Down: "Down",
            dpg.mvKey_Insert: "Insert",
            dpg.mvKey_Delete: "Delete",
            dpg.mvKey_Prior: "Prior",
            dpg.mvKey_Next: "Next",
            # Miscellaneous Keys
            dpg.mvKey_None: "None",
            dpg.mvKey_Pause: "Pause",
            dpg.mvKey_CapsLock: "CapsLock",
            dpg.mvKey_Escape: "Escape",
            dpg.mvKey_Print: "Print",
            dpg.mvKey_NumLock: "NumLock",
            dpg.mvKey_ScrollLock: "ScrollLock",
            dpg.mvKey_Period: "period",
            dpg.mvKey_Slash: "slash",
            dpg.mvKey_Backslash: "backslash",
            dpg.mvKey_Open_Brace: "bracketleft",
            dpg.mvKey_Close_Brace: "bracketright",
            dpg.mvKey_Browser_Back: "Browser_Back",
            dpg.mvKey_Browser_Forward: "Browser_Forward",
            dpg.mvKey_Comma: "comma",
            dpg.mvKey_Minus: "minus",
            602: "equal",
            dpg.mvKey_Menu: "Menu",
            dpg.mvKey_Clear: "Clear",
            dpg.mvKey_Select: "Select",
            dpg.mvKey_Execute: "Execute",
            dpg.mvKey_Apps: "Apps",
            dpg.mvKey_Sleep: "Sleep",
            dpg.mvKey_Help: "Help",
            dpg.mvKey_Browser_Refresh: "Browser_Refresh",
            dpg.mvKey_Browser_Stop: "Browser_Stop",
            dpg.mvKey_Browser_Search: "Browser_Search",
            dpg.mvKey_Browser_Favorites: "Browser_Favorites",
            dpg.mvKey_Browser_Home: "Browser_Home",
            dpg.mvKey_Volume_Mute: "Volume_Mute",
            dpg.mvKey_Volume_Down: "Volume_Down",
            dpg.mvKey_Volume_Up: "Volume_Up",
            dpg.mvKey_Media_Next_Track: "Media_Next_Track",
            dpg.mvKey_Media_Prev_Track: "Media_Prev_Track",
            dpg.mvKey_Media_Stop: "Media_Stop",
            dpg.mvKey_Media_Play_Pause: "Media_Play_Pause",
            dpg.mvKey_Launch_Mail: "Launch_Mail",
            dpg.mvKey_Launch_Media_Select: "Launch_Media_Select",
            dpg.mvKey_Launch_App1: "Launch_App1",
            dpg.mvKey_Launch_App2: "Launch_App2",
            dpg.mvKey_Colon: "Colon",
            dpg.mvKey_Plus: "Plus",
            dpg.mvKey_Tilde: "Tilde",
            dpg.mvKey_Quote: "Quote"
        }        
        return map.get(keycode)
