import os
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


async def run_rtc(frame_queue, control_queue):
    # Create rtc api
    rtc = RTCApi(is_offer=True, frame_queue=frame_queue, control_queue=control_queue) 

    sdp = await rtc.createSession()

    js = {"sdp": sdp}
    response = requests.post(f"{SERVER_ENDPOINT}/add-offer-sdp", json=js)

    js = response.json()
    sdp = js["sdp"]
    
    await rtc.acceptAnswer(sdp)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await rtc.shutdown()

def start_rtc(frame_queue, control_queue):
    def target():
        asyncio.run(run_rtc(frame_queue, control_queue))

    rtc_thread = threading.Thread(target=target, daemon=True)
    rtc_thread.start()

def start_gui(frame_queue, control_input):
    gui = Dearpygui("MainView", 1300, 820, frame_queue, control_input)
    gui.init_gui()

def main():
    # Create queue of frames to deliver between RTC and GUI
    frame_queue = queue.Queue(maxsize=4)
    control_queue = queue.Queue()

    def on_input(message):
        msg = json.dumps(message)
        control_queue.put_nowait(msg)
        print("INPUT:", msg)

    input = Input(on_input)

    start_rtc(frame_queue, control_queue)
    start_gui(frame_queue, input)


if ( __name__ == "__main__"):
    main()
