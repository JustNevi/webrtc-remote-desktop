import dearpygui.dearpygui as dpg

from components.gui.windows.window import Window
from components.gui.windows.main_window import MainWindow

class Dearpygui:
    def __init__(self, title, width, height, frame_queue):
        self.title = title
        self.width = width 
        self.height = height

        self.frame_queue = frame_queue

    def init_gui(self):
        windows = self.setup_windows()
        
        # Dearpygui setup
        dpg.create_context()
        dpg.create_viewport(title=self.title, width=self.width, height=self.height)

        # Init windows and render components
        for window in windows:
            window.render()

        dpg.setup_dearpygui()
        dpg.show_viewport()

        # Dearpygui render loop.
        # All inside runs every frame.
        while dpg.is_dearpygui_running():
            # Make all needed updates in windows
            for window in windows:
                window.update()

            dpg.render_dearpygui_frame()    

        dpg.destroy_context()

    def setup_windows(self):
        windows: list[Window] = []

        windows.append(MainWindow("MainWindow", self.width, self.height, self.frame_queue))
        
        return windows  

