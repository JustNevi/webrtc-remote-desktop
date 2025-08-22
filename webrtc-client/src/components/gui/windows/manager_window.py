import time
import queue
import logging
import asyncio
import requests
import threading

from components.rtc.rtc_api import RTCApi
from components.rtc.inputs.input import Input 

import dearpygui.dearpygui as dpg

from components.gui.windows.window import Window

class ManagerWindow(Window):
    def __init__(self, endpoint):
        # View
        self.label = "ManagerWindow"
        self.width = 50 
        self.height = 100

        self.endpoint = endpoint

        # Queues
        # Create queue of frames to deliver between RTC and GUI
        self.frame_queue = queue.Queue(maxsize=4)
        # Create queue of controls to handle inputs from GUI and send to RTC 
        self.control_queue = queue.Queue()

        # Input controller
        self.control_input = Input(self.control_input_callback)

        # Events
        self.rtc_async_loop = None
        self.rtc_close_event = asyncio.Event()

        self.rtc_thread = None

        self.rtc = RTCApi(
            is_offer=True, 
            frame_queue=self.frame_queue, 
            control_queue=self.control_queue
        )

        # Logging
        self.logger = logging.getLogger(self.__class__.__name__)

        # Tags
        self.setup_tags()

    def setup_tags(self):
        self.TAG = self.__class__.__name__

        def make_tag(name):
            return f"{self.TAG}_{name}"

        self.TAG_BTN_CONNECT = make_tag("btn_connect")

    def get_frame_queue(self):
        return self.frame_queue

    def get_control_input(self):
        return self.control_input


    def render(self):
        with dpg.window(
                tag=self.TAG, 
                label=self.label, 
                width=self.width, 
                height=self.height,
                no_resize=True,
                on_close=self.close_callback
            ):
            dpg.add_button(
                tag=self.TAG_BTN_CONNECT,
                label="Connect", 
                callback=self.connect_callback
            )

    ## GUI handlers
    def connect_callback(self, sender, data):
        if (self.is_rtc_running()):
            self.stop_rtc()
            dpg.set_item_label(item=self.TAG_BTN_CONNECT, label="Connect")
        else: 
            self.start_rtc()
            dpg.set_item_label(item=self.TAG_BTN_CONNECT, label="Disconnect")

    def close_callback(self, sender):
        self.stop_rtc() 


    # Handle messages from inputs controller
    def control_input_callback(self, message):
        self.control_queue.put_nowait(message)
        self.logger.debug(message)

    def is_rtc_running(self):
        if (self.rtc_thread):
            return self.rtc_thread.is_alive()
        return False


    # Start rtc thread
    def start_rtc(self):
        # Clear the close event to wait until it is disconnected again        
        self.rtc_close_event.clear()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def target():
            loop.run_until_complete(
                self.run_rtc()
            )

        # Start rtc thread
        self.rtc_thread = threading.Thread(target=target, daemon=True)
        self.rtc_thread.start()

        # Store loop to send events in future
        self.rtc_async_loop = loop 

    def stop_rtc(self):
        if (self.rtc_async_loop):
            self.logger.info("Stopping RTC...")
            # Set close event
            self.rtc_async_loop.call_soon_threadsafe(self.rtc_close_event.set)
            # Wait for rtc peer connection closes
            time.sleep(1)

    # Run async rtc client
    async def run_rtc(self):
        # Create rtc api
        self.rtc.init_peer_connection()

        sdp = await self.rtc.createSession()

        js = {"sdp": sdp}
        response = requests.post(f"{self.endpoint}/add-offer-sdp", json=js)

        js = response.json()
        sdp = js["sdp"]
        
        await self.rtc.acceptAnswer(sdp)

        try:
            await self.rtc_close_event.wait()
        finally:
            await self.rtc.shutdown()
            self.logger.info("RTC shutdown complete.")
