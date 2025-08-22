import cv2
import numpy as np
from av import VideoFrame

import dearpygui.dearpygui as dpg

from components.gui.windows.window import Window

class MainWindow(Window):

    # 655 - left click
    # 656 - right click
    # 657 - middle click
    # 661 - scroll vertical  
    # 660 - scroll horisontal  
    IGNORED_KEYS = frozenset([655, 656, 657, 661, 660])

    def __init__(self, width, height, frame_queue, control_input):
        # View
        self.label = "MainWindow" 
        self.width = width
        self.height = height

        # Video frame queue
        self.frame_queue = frame_queue
        self.frame_size = (self.width, self.height) 
        self.texture_created = False
        self._texture_buffer = None
        self._rgb_buffer = None

        # Control input management
        self.control_input = control_input
        self.mouse_is_down = False
        
        # Tags
        self.setup_tags()

    def setup_tags(self):
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

        with dpg.window(
                tag=self.TAG, 
                label=self.label, 
                width=self.width, height=self.height,
                no_resize=True
            ):
            dpg.add_text("Waiting for video stream...", tag=self.TAG_INFO)

        # Input handlers
        self.register_mouse_handlers()
        self.register_keyboard_handlers()

    def update(self):
        self.update_frame() 

    # Update frames in image
    def update_frame(self):
        if (not self.frame_queue.empty()):
            video_frame = self.frame_queue.get_nowait()

            texture_data, width, height = self.convert_video_frame_into_texture_data(video_frame) 

            # Create dynmic texture to render frames and setup size
            self.setup_display(width, height)

            # If frame size changes - update window size
            self.update_window_size(width, height)

            # Display the image
            if dpg.does_item_exist(self.TAG_TEXTURE):
                dpg.set_value(self.TAG_TEXTURE, texture_data)

    def setup_display(self, width, height):
        if (not self.texture_created):
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

            self.texture_created = True

    def get_image_margin(self):
        # Get image position on this window (title height included)
        image_pos = dpg.get_item_pos(self.TAG_IMAGE)

        # This is actually image top-left position without title height (custom solution)
        offset = (image_pos[0], image_pos[1])

        return offset

    def update_window_size(self, width, height):
        if (self.frame_size != (width, height)):
            margin = self.get_image_margin()
            if (margin != (0, 0)):
                self.frame_size = (width, height)

                margin = (margin[0] * 2, margin[1] * 1.5)

                self.width = self.frame_size[0] + margin[0]
                self.height = self.frame_size[1] + margin[1]

                # Set windows size
                dpg.set_item_width(self.TAG, self.width)
                dpg.set_item_height(self.TAG, self.height)
                # Set viewport size
                dpg.set_viewport_width(self.width)
                dpg.set_viewport_height(self.height)

    def convert_video_frame_into_texture_data(self, frame: VideoFrame):
        img = frame.to_ndarray(format="bgr24")
        height, width = img.shape[:2]
        
        # Reuse buffers to avoid memory allocation overhead
        buffer_size = height * width * 3
        
        if self._rgb_buffer is None or self._rgb_buffer.size != buffer_size:
            self._rgb_buffer = np.empty((height, width, 3), dtype=np.uint8)
            self._texture_buffer = np.empty(buffer_size, dtype=np.float32)
        
        # Use pre-allocated buffer for BGR to RGB conversion
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, dst=self._rgb_buffer)
        
        # Vectorized normalization and flattening in one step
        np.multiply(self._rgb_buffer, 1.0/255.0, out=self._texture_buffer.reshape(height, width, 3), casting='unsafe')
        
        return self._texture_buffer, width, height

    # Register mouse events to get mouse position
    def register_mouse_handlers(self):
        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=self.mouse_move_callback)
            dpg.add_mouse_down_handler(callback=self.mouse_down_callback)
            dpg.add_mouse_release_handler(callback=self.mouse_release_callback)
            #dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left, callback=self.mouse_drag_callback)
            #dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Right, callback=self.mouse_drag_callback)
            dpg.add_mouse_wheel_handler(callback=self.mouse_wheel_callback)

    def image_exists(func):
        def wrapper(self, sender, data, *args, **kwargs):
            if (self.texture_created):
                func(self, sender, data, *args, **kwargs)
        return wrapper

    @image_exists
    def mouse_move_callback(self, sender, data):
        # "data" is position 
        image_pos = self.get_on_image_position(data) 

        self.control_input.mouse.move(image_pos)

    @image_exists
    def mouse_down_callback(self, sender, data):
        if (self.mouse_is_down):
            return
        self.mouse_is_down = True

        # "data[0]" is the mouse button (0=Left, 1=Right, 2=Middle)
        # "data[1]" is time 
        button = data[0]
        pos = dpg.get_mouse_pos()

        image_pos = self.get_on_image_position(pos) 

        self.control_input.mouse.down(button, image_pos)

    @image_exists
    def mouse_release_callback(self, sender, data):
        self.mouse_is_down = False 

        # "data" is the mouse button (0=Left, 1=Right, 2=Middle)
        button = data 
        pos = dpg.get_mouse_pos()

        image_pos = self.get_on_image_position(pos) 

        self.control_input.mouse.release(button, image_pos)

    @image_exists
    def mouse_drag_callback(self, sender, data):
        # "data" is a list: [button, drag_delta_x, drag_delta_y]
        button = data[0]
        delta_pos = (data[1], data[2])
        pos = dpg.get_mouse_pos()

        image_pos = self.get_on_image_position(pos) 

        self.control_input.mouse.drag(button, image_pos, delta_pos)

    @image_exists
    def mouse_wheel_callback(self, sender, data):
        self.control_input.mouse.scroll(3, data)

    # Calculate position on image related to local window position
    def get_on_image_position(self, position):
        # Get this window position
        window_pos = dpg.get_item_pos(self.TAG)

        # Image top-left position without title height (custom solution)
        margin = self.get_image_margin()

        return (
            int(position[0] - margin[0] - window_pos[0]), 
            int(position[1] - margin[1] - window_pos[1])
        )

         
    # Register keyboard events to get keys inputs 
    def register_keyboard_handlers(self):
        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=self.keyboard_press_callback)
            dpg.add_key_release_handler(callback=self.keyboard_release_callback)

    def key_ignore(func):
        def wrapper(self, sender, data, *args, **kwargs):

            if (data not in self.IGNORED_KEYS):
                func(self, sender, data, *args, **kwargs)
        return wrapper

    @key_ignore
    def keyboard_press_callback(self, sender, data):
        # "data" is key code
        self.control_input.keyboard.press(data)

    @key_ignore
    def keyboard_release_callback(self, sender, data):
        # "data" is key code
        self.control_input.keyboard.release(data)
