import time
import cv2
import mss
import numpy as np
from av import VideoFrame
from fractions import Fraction

from aiortc.mediastreams import VideoStreamTrack

from components.rtc.tracks.screen_capture_track import ScreenCaptureTrack

class ScreenCaptureTrack(VideoStreamTrack):
    """
    A video stream track that captures the screen.
    """
    def __init__(self, fps=30):
        super().__init__()
        self.sct = mss.mss() # Initialize mss for screen capture
        self.monitor = self.sct.monitors[1] # Capture the primary monitor
        self.fps = fps

    async def recv(self):
        """
        Capture a frame from the screen and return it as a VideoFrame.
        """
        # Get a screen shot
        screenshot = self.sct.grab(self.monitor)

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
        frame.time_base = Fraction(1, 1000) # <-- Corrected line

        # Wait for the next frame
        await asyncio.sleep(1 / self.fps)  # Adjust this for desired frame rate (e.g., 30 FPS)
        
        return frame
