import dearpygui.dearpygui as dpg

from components.gui.windows.window import Window
from components.gui.windows.main_window import MainWindow
from components.gui.windows.manager_window import ManagerWindow

class Dearpygui:
    def __init__(self, title, width, height, endpoint):
        self.title = title
        self.width = width 
        self.height = height

        self.endpoint = endpoint

        self.windows: list[Window] = []

    def init_gui(self):
        # Create and setup windows
        self.setup_windows()

        # Dearpygui setup
        dpg.create_context()
        dpg.create_viewport(title=self.title, width=self.width, height=self.height)

        # Init windows and render components
        for window in self.windows:
            window.render()

        dpg.setup_dearpygui()
        dpg.show_viewport()

        # Dearpygui render loop.
        # All inside runs every frame.
        while dpg.is_dearpygui_running():
            # Make all needed updates in windows
            for window in self.windows:
                window.update()

            dpg.render_dearpygui_frame()    

        dpg.destroy_context()

    def setup_windows(self):
        self.windows = []

        manager = ManagerWindow(self.endpoint)

        main = MainWindow(
            self.width, 
            self.height, 
            manager.get_frame_queue(), 
            manager.get_control_input()
        )

        self.windows.extend([
            main,
            manager
        ])

    def close(self):
        self.windows[1].stop_rtc()
