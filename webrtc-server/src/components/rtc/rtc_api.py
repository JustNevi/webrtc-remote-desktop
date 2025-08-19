import time
import asyncio
import logging
import queue

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.mediastreams import VideoStreamTrack

from components.rtc.tracks.screen_capture_track import ScreenCaptureTrack

class RTCApi:
    def __init__(
            self, 
            is_offer=True, 
            frame_queue: queue.Queue=None, 
            control_queue: queue.Queue=None, 
            on_message=lambda msg: print(msg), 
            do_logging=True
        ):
        self.pc = None 
        self.is_offer = is_offer

        # Dist session description
        self.sdp_local = None
        self.sdp_remote = None

        # Datachannel
        self.datachannel = None
        self.on_message = on_message

        # Control
        self.control_transferring = True
        self.control_queue = control_queue

        # Track
        self.frame_receiving = True
        self.frame_queue = frame_queue 

        # Logging
        self.logger = None
        self.setup_logger(do_logging)

    # Create peerconnection and setup events
    def init_peer_connection(self):
        # If peer connection has already been created - close it. 
        if (self.pc):
            asyncio.create_task(self.shutdown())

        # Create peer connection
        self.pc = RTCPeerConnection()

        if (not self.is_offer):
            # Setup tracks
            self.pc.addTrack(ScreenCaptureTrack(fps=120))
        else:
            self.pc.addTrack(VideoStreamTrack())

        @self.pc.on("connectionstatechange")
        async def on_connection_state_change():
            if (self.pc):
                state = self.pc.connectionState
                self.logger.info(f"Connection state is *{state}*.")

                # Close everything if connection state is closed
                if (state == "closed"):
                    await self.shutdown()

        @self.pc.on("track")
        def on_track(track):
            if track.kind == "video":
                self.logger.info("Incoming video track received.")

                if (self.frame_queue):
                    async def receiver():
                        while (self.frame_receiving):
                            # from av import VidioFrame 
                            frame = await track.recv()

                            # Empty all old frames 
                            while not self.frame_queue.empty():
                                self.frame_queue.get_nowait()

                            self.frame_queue.put_nowait(frame)

                    asyncio.create_task(receiver())

        self.init_datachannel()

    # Create or handle event
    def init_datachannel(self):
        if (self.is_offer):
            self.datachannel = self.pc.createDataChannel("control")
            self.setup_datachannel(self.datachannel)
        else:
            @self.pc.on("datachannel")
            def on_datachannel(channel):
                self.datachannel = channel
                self.setup_datachannel(self.datachannel)

    # Set up events for datachannel
    def setup_datachannel(self, datachannel):
        @datachannel.on("open")
        def on_open():
            self.logger.info("Data channel is open.")

        @datachannel.on("message")
        def on_message(message):
            # Handle messages for processing in control input thread
             if (self.control_queue):
                if (self.control_transferring):
                    self.control_queue.put_nowait(message)
                    time.sleep(0.004)

        @datachannel.on("close")
        def on_close():
            self.logger.info("Data channel is closed.")

    async def createSession(self, offer=None):
        sdp = None
        if (self.is_offer):
            sdp = await self.pc.createOffer()
        else:
            if (offer):
                offer_sdp = RTCSessionDescription(
                    sdp=offer["sdp"],
                    type=offer["type"]
                )
                await self.pc.setRemoteDescription(offer_sdp)
                self.sdp_remote = offer
                self.logger.info("The offer was accepted.")

                sdp = await self.pc.createAnswer()
            else:
                raise Exception("If you answer, you must provide offer.")

        await self.pc.setLocalDescription(sdp)
        self.logger.info("Local session has been established.")

        self.sdp_local = {
            "sdp": self.pc.localDescription.sdp,
            "type": self.pc.localDescription.type
        }
        return self.sdp_local

    async def acceptAnswer(self, answer):
        if (self.is_offer):
            answer_sdp = RTCSessionDescription(
                sdp=answer["sdp"],
                type=answer["type"]
            )
            await self.pc.setRemoteDescription(answer_sdp)
            self.sdp_remote = answer 
            self.logger.info("The answer was accepted.")


    async def shutdown(self):
        if (self.pc):
            if (self.datachannel):
                self.datachannel.close()
                self.logger.info("Datachannel closed.")

            await self.pc.close()
            self.pc = None
            self.logger.info("RTCPeerConnection closed.")

    def setup_logger(self, do_logging):
        name = self.__class__.__name__

        self.logger = logging.getLogger(name)
        if (not do_logging):
            self.logger.addFilter(logging.Filter(name))
