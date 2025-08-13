import cv2
import numpy as np
from av import VideoFrame

import dearpygui.dearpygui as dpg

from components.gui.windows.window import Window

class MainWindow(Window):
    def __init__(self, lable, width, height, frame_queue):
        # View
        self.lable = lable
        self.width = width
        self.height = height

        # Video frame queue
        self.frame_queue = frame_queue
        
        # Tags
        self.TAG = self.__class__.__name__
        def make_tag(name):
            return f"{self.TAG}_{name}"
        self.TAG_INFO = make_tag("info")
        self.TAG_TEXTURE_REGISTER = make_tag("texture_register") 
        self.TAG_TEXTURE = make_tag("texture")
        self.TAG_IMAGE = make_tag("image")

    def render(self):
        with dpg.texture_registry(tag=self.TAG_TEXTURE_REGISTER):
            pass

        with dpg.window(tag=self.TAG, label=self.lable, width=self.width, height=self.height):
            dpg.add_text("Waiting for video stream...", tag=self.TAG_INFO)

        self.register_mouse_handlers()

    def update(self):
        self.update_frame() 

    # Update frames in image
    def update_frame(self):
        if (not self.frame_queue.empty()):
            video_frame = self.frame_queue.get_nowait()

            texture_data, width, height = self.convert_video_frame_into_texture_data(video_frame) 

            # Create dynmic texture to render frames and setup size
            self.setup_display(width, height)

            # Display the image
            if dpg.does_item_exist(self.TAG_TEXTURE):
                dpg.set_value(self.TAG_TEXTURE, texture_data)

    def setup_display(self, width, height):
        if (not dpg.does_item_exist(self.TAG_TEXTURE)):
            # Delete information to replace with image
            dpg.delete_item(self.TAG_INFO)

            # Create texture and image to render frames
            dpg.add_raw_texture(
                tag=self.TAG_TEXTURE, 
                width=width, 
                height=height, 
                default_value=[],
                format=dpg.mvFormat_Float_rgb,
                parent=self.TAG_TEXTURE_REGISTER
            )
            dpg.add_image(
                self.TAG_TEXTURE,
                tag=self.TAG_IMAGE,
                parent=self.TAG
            )

    def convert_video_frame_into_texture_data(self, frame: VideoFrame):
        img = frame.to_ndarray(format="bgr24")
        
        # Convert BGR to RGB for DearPyGUI
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize to 0-1 range for DearPyGUI (it expects float values)
        img_normalized = img_rgb.astype(np.float32) / 255.0
        
        # Flatten the array for DearPyGUI texture
        img_flat = img_normalized.flatten()
        
        # Get dimensions
        height, width = img_rgb.shape[:2]

        return img_flat, width, height

    # Register mouse events to get mouse position
    def register_mouse_handlers(self):
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=self.mouse_down_callback)
            dpg.add_mouse_release_handler(callback=self.mouse_release_callback)
            dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left, callback=self.mouse_drag_callback)
            dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Right, callback=self.mouse_drag_callback)

    def mouse_down_callback(self, sender, data):
        # data[0] is the mouse button (0=Left, 1=Right, 2=Middle)
        pos = dpg.get_mouse_pos()
        image_pos = self.get_on_image_position(pos) 
        print("Down", pos, image_pos)

    def mouse_release_callback(self, sender, data):
        # data[0] is the mouse button (0=Left, 1=Right, 2=Middle)
        pos = dpg.get_mouse_pos()
        print("Release", pos)

    def mouse_drag_callback(self, sender, data):
        # data is a list: [button, drag_delta_x, drag_delta_y]
        pos = dpg.get_mouse_pos()
        print("Drag", pos, data[0])

    # Calculate position on image related to local window position
    def get_on_image_position(self, position):
        # Get image position on this window (title height included)
        image_pos = dpg.get_item_pos(self.TAG_IMAGE)

        # This is actually image top-left position without title height (custom solution)
        offset = (image_pos[0], image_pos[0])

        return (position[0] - offset[0], position[1] - offset[1])

         
