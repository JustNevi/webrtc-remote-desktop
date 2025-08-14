import os
import asyncio
import logging

from components.rtc.rtc_api import RTCApi
from components.rtc.inputs.input import Input 

from quart import Quart, request, jsonify

# Env
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

HOST = os.getenv("RTC_RD_HOST") 
PORT = os.getenv("RTC_RD_PORT") 
DEBUG = os.getenv("RTC_RD_DEBUG") 

# Logging
logging.basicConfig(level=logging.INFO)

# Setup rtc api
rtc_api = None 

# Setup Quart 
app = Quart(__name__)

@app.before_serving
async def create_rtc_api():
    global rtc_api
    input = Input()
    rtc_api = RTCApi(is_offer=False, on_message=input.on_message)

@app.after_serving
async def shutdown_rtc_api():
    global rtc_api
    if (rtc_api):
        await rtc_api.shutdown()
        rtc_api = None

@app.route("/add-offer-sdp", methods=["POST"])
async def add_offer_sdp():
    global rtc_api
    if (not rtc_api):
        return jsonify({"error": "RTC API not initialized"}), 503

    data = await request.get_json()

    sdp = data.get("sdp")
    
    answer = await rtc_api.createSession(sdp)

    return jsonify({"sdp": answer})


if ( __name__ == "__main__"):
    app.run(host=HOST, port=PORT, debug=DEBUG)
