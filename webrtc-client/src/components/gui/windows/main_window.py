import cv2
import numpy as np
from av import VideoFrame

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
        self.TEXTURE_REGISTER_TAG = make_tag("texture_register") 
        self.TEXTURE_TAG = make_tag("texture")
        self.IMAGE_TAG = make_tag("image")

    def render(self, dpg):
        with dpg.texture_registry(tag=self.TEXTURE_REGISTER_TAG):
            pass

        with dpg.window(tag=self.TAG, label=self.lable, width=self.width, height=self.height):
            dpg.add_text("Waiting for video stream...")

    def update(self, dpg):
        self.update_frame(dpg) 

    # Update frame in image
    def update_frame(self, dpg):
        if (not self.frame_queue.empty()):
            video_frame = self.frame_queue.get_nowait()

            texture_data, width, height = self._convert_video_frame_into_texture_data(dpg, video_frame) 

            # Create dynmic texture to render frame and setup size
            self.setup_display(dpg, width, height)

            # Display the image
            if dpg.does_item_exist(self.TEXTURE_TAG):
                dpg.set_value(self.TEXTURE_TAG, texture_data)

    def setup_display(self, dpg, width, height):
        if (not dpg.does_item_exist(self.TEXTURE_TAG)):
            dpg.add_raw_texture(
                tag=self.TEXTURE_TAG, 
                width=width, 
                height=height, 
                default_value=[],
                format=dpg.mvFormat_Float_rgb,
                parent=self.TEXTURE_REGISTER_TAG
            )
            dpg.add_image(
                self.TEXTURE_TAG,
                tag=self.IMAGE_TAG,
                parent=self.TAG
            )

    def _convert_video_frame_into_texture_data(self, dpg, frame: VideoFrame):
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
