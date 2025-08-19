import os
import time
import json
import queue
import threading
import logging
import asyncio
import requests

from components.rtc.rtc_api import RTCApi
from components.rtc.inputs.input import Input 

from components.gui.gui import Dearpygui

from dotenv import load_dotenv
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

# Env variables
SERVER_IP = os.getenv("SERVER_IP") 
SERVER_PORT = os.getenv("SERVER_PORT") 
SERVER_ENDPOINT = f"http://{SERVER_IP}:{SERVER_PORT}"


async def run_rtc(frame_queue, control_queue, close_event):
    # Create rtc api
    rtc = RTCApi(is_offer=True, frame_queue=frame_queue, control_queue=control_queue) 
    rtc.init_peer_connection()

    sdp = await rtc.createSession()

    js = {"sdp": sdp}
    response = requests.post(f"{SERVER_ENDPOINT}/add-offer-sdp", json=js)

    js = response.json()
    sdp = js["sdp"]
    
    await rtc.acceptAnswer(sdp)

    try:
        await close_event.wait()
    finally:
        await rtc.shutdown()
        logging.info("RTC shutdown complete.")

def start_rtc(frame_queue, control_queue, close_event):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def target():
        loop.run_until_complete(run_rtc(frame_queue, control_queue, close_event))

    rtc_thread = threading.Thread(target=target, daemon=True)
    rtc_thread.start()
    return loop

def start_gui(frame_queue, control_input):
    gui = Dearpygui("MainView", 1320, 840, frame_queue, control_input)
    # The program stops here until the window is closed.
    gui.init_gui()


def main():
    # Create queue of frames to deliver between RTC and GUI
    frame_queue = queue.Queue(maxsize=4)
    control_queue = queue.Queue()

    def on_input(message):
        control_queue.put_nowait(message)
        print("INPUT:", message)

    input = Input(on_input)

    close_event = asyncio.Event()

    # === Start ===
    loop = start_rtc(frame_queue, control_queue, close_event)
    start_gui(frame_queue, input)

    # === End ===
    # Runs when windows are closed 
    loop.call_soon_threadsafe(close_event.set)
    # Wait for rtc peer connection closes
    time.sleep(1)


if ( __name__ == "__main__"):
    main()
