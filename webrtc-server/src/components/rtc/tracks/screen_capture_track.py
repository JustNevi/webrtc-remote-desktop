import asyncio
import time
import cv2
import mss
import numpy as np
from av import VideoFrame
from fractions import Fraction

from aiortc.mediastreams import VideoStreamTrack

class ScreenCaptureTrack(VideoStreamTrack):
    """
    A video stream track that captures the screen efficiently.
    """
    def __init__(self, fps=30):
        super().__init__()
        self.monitor = None
        self.fps = fps
        self.sct = mss.mss()
        self.sct_monitor = self.sct.monitors[1]
        self._last_capture_time = 0

    async def recv(self):
        # Await the next frame based on the desired FPS
        now = time.time()
        if self._last_capture_time:
            wait_time = (1.0 / self.fps) - (now - self._last_capture_time)
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        # Capture a single frame from the screen
        screenshot = self.sct.grab(self.sct_monitor)
        self._last_capture_time = time.time()

        # Convert the screenshot to a VideoFrame
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        frame = VideoFrame.from_ndarray(img, format="bgr24")

        # Set the timestamp and time base
        pts = int(self._last_capture_time * 1000)
        frame.pts = pts
        frame.time_base = Fraction(1, 1000)
        
        return frame
