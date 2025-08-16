import asyncio
import time
import threading
import queue
import cv2
import mss
import numpy as np
from av import VideoFrame
from fractions import Fraction

from aiortc.mediastreams import VideoStreamTrack

class ScreenCaptureTrack(VideoStreamTrack):
    """
    A video stream track that captures the screen.
    """
    def __init__(self, fps=30):
        super().__init__()
        self.monitor = None 
        self.fps = fps


        self.running = True
        self.queue = queue.Queue(maxsize=4)
        self.thread = threading.Thread(target=self.capture, daemon=True)

        self.start()

    def start(self):
        self.thread.start()

    def capture(self):
        with mss.mss() as sct:
            self.monitor = sct.monitors[1]
            while (self.running):
                """
                Capture a frame from the screen and return it as a VideoFrame.
                """
                # Get a screen shot
                screenshot = sct.grab(self.monitor)

                # Convert screenshot to a NumPy array
                img = np.array(screenshot)

                # Convert the image from BGRA to BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Create a PyAV VideoFrame from the NumPy array
                frame = VideoFrame.from_ndarray(img, format="bgr24")
                
                # Set the timestamp for the frame
                pts = int(time.time() * 1000)
                frame.pts = pts
                
                # Set the time base (e.g., 1/1000)
                frame.time_base = Fraction(1, 1000)
                
                # Empty all old frames 
                while (not self.queue.empty()):
                    self.queue.get_nowait()
                
                self.queue.put_nowait(frame)

                # Control the frame rate
                time.sleep(1 / self.fps)

    async def recv(self):
        return self.queue.get() 
