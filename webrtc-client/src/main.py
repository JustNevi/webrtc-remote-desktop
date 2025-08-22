import os
import time
import logging

from components.gui.gui import Dearpygui

from dotenv import load_dotenv
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

# Env variables
SERVER_IP = os.getenv("SERVER_IP") 
SERVER_PORT = os.getenv("SERVER_PORT") 
SERVER_ENDPOINT = f"http://{SERVER_IP}:{SERVER_PORT}"

def start_gui():
    gui = Dearpygui("MainView", 1320, 840, SERVER_ENDPOINT)
    # The program stops here until the window is closed.
    gui.init_gui()

    # Runs after viewport closed
    logging.info("Closing...")
    gui.close()
    time.sleep(1)

def main():
    # === Start ===
    start_gui()


if ( __name__ == "__main__"):
    main()
