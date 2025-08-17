import asyncio
import mss
import numpy as np
from av import VideoFrame
from aiortc import VideoStreamTrack

class ScreenCaptureTrack(VideoStreamTrack):
    def __init__(self, fps=30, monitor=1, region=None, width=None, height=None, pix_fmt="yuv420p"):
        super().__init__()
        self.fps = fps
        self._sct = mss.mss()
        self._monitor = region if region is not None else self._sct.monitors[monitor]
        self._out_w = width
        self._out_h = height
        self._pix_fmt = pix_fmt

    async def recv(self) -> VideoFrame:
        # Pacing / timestamps managed by aiortc
        pts, time_base = await self.next_timestamp()

        shot = self._sct.grab(self._monitor)  # raw BGRA bytes, width=shot.width, height=shot.height

        # Wrap raw BGRA buffer without extra copy
        arr = np.frombuffer(shot.raw, dtype=np.uint8)
        arr = arr.reshape((shot.height, shot.width, 4))

        frame = VideoFrame.from_ndarray(arr, format="bgra")

        # Optional resize + pixel format convert using libswscale (fast, in C)
        target_w = self._out_w or frame.width
        target_h = self._out_h or frame.height
        target_fmt = self._pix_fmt or frame.format.name  # keep bgra if None

        if (target_w != frame.width) or (target_h != frame.height) or (target_fmt != frame.format.name):
            frame = frame.reformat(width=target_w, height=target_h, format=target_fmt)

        frame.pts = pts
        frame.time_base = time_base
        return frame

    async def close(self):
        # Clean up mss resources
        try:
            self._sct.close()
        except Exception:
            pass
        await super().stop()

