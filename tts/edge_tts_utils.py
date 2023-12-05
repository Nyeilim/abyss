import asyncio
import io
import logging
import re
import time
import uuid

import websockets
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

# 全局变量
LOGGER = logging.getLogger("tts")
LOGGER.setLevel(level=logging.INFO)
TIME_INTERVAL = 5
tts_texts = asyncio.Queue()
text_cache = ""
last_submit_time = int(time.time())


# Generate SSML.xml
def gen_ssml(tts_text):
    return f'''
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="zh-CN-XiaoxiaoNeural">
            <prosody rate="0%" pitch="0%">
                {tts_text}
            </prosody>
        </voice>
    </speak>
    '''


# Generate Unique Request Id
def get_req_id():
    return uuid.uuid4().hex.upper()


# Fix the time to match Americanisms
def hr_cr(hr):
    corrected = (hr - 1) % 24
    return str(corrected)


# Add zeros in the right places i.e 22:1:5 -> 22:01:05
def fr(input_string):
    corr = ''
    i = 2 - len(input_string)
    while i > 0:
        corr += '0'
        i -= 1
    return corr + input_string


# Generate X-Timestamp all correctly formatted
# noinspection DuplicatedCode
def get_x_timestamp():
    now = datetime.now()
    return fr(str(now.year)) \
           + '-' + fr(str(now.month)) \
           + '-' + fr(str(now.day)) \
           + 'T' + fr(hr_cr(int(now.hour))) \
           + ':' + fr(str(now.minute)) \
           + ':' + fr(str(now.second)) \
           + '.' + str(now.microsecond)[:3] + 'Z'


# Put tts text to global variables
def put_tts_text(text):
    cur_time = int(time.time())
    if cur_time - last_submit_time > TIME_INTERVAL and text_cache != text:
        tts_texts.put(text)
    else:
        LOGGER.info(f"text submitted recently, cancel request. args: {text}")


# Get tts text to global variables
def get_tts_text():
    if tts_texts.empty():
        return None
    else:
        return tts_texts.get()


# Request
async def transfer_data(ssml):
    # Params Construction
    req_id = get_req_id()
    TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"
    WSS_URL = (
            "wss://speech.platform.bing.com/consumer/speech/synthesize/"
            + "readaloud/edge/v1?TrustedClientToken="
            + TRUSTED_CLIENT_TOKEN
    )
    endpoint = f"{WSS_URL}&ConnectionId={req_id}"

    # Send Request
    async with websockets.connect(endpoint, extra_headers={
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Origin": "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41"}) as websocket:
        auth_msg = (
            f"X-Timestamp:{get_x_timestamp()}\r\n"
            "Content-Type:application/json; charset=utf-8\r\n"
            "Path:speech.config\r\n\r\n"
            '{"context":{"synthesis":{"audio":{"metadataoptions":{'
            '"sentenceBoundaryEnabled":false,"wordBoundaryEnabled":true},'
            '"outputFormat":"audio-24khz-48kbitrate-mono-mp3"'
            "}}}}\r\n"
        )
        await websocket.send(auth_msg)

        data_msg = (
            f"X-RequestId:{req_id}\r\n"
            "Content-Type:application/ssml+xml\r\n"
            f"X-Timestamp:{get_x_timestamp()}Z\r\n"  # This is not a mistake, Microsoft Edge bug.
            "Path:ssml\r\n\r\n"
            f"{ssml}")
        await websocket.send(data_msg)

        # Checks for close connection message
        end_resp_pat = re.compile('Path:turn.end')
        audio_stream = b''
        while True:
            response = await websocket.recv()
            print('receiving...')
            # print(response)
            # Make sure the message isn't telling us to stop
            if re.search(end_resp_pat, str(response)) is None:
                # Check if our response is text data or the audio bytes
                if isinstance(response, bytes):
                    # Extract binary data
                    try:
                        needle = b'Path:audio\r\n'
                        start_ind = response.find(needle) + len(needle)
                        audio_stream += response[start_ind:]
                    except Exception as e:
                        LOGGER.info(f"exception: {e}")
            else:
                break

        # Data is audio_stream
        audio = AudioSegment.from_file(io.BytesIO(audio_stream), format='mp3')
        play(audio)  # Play audio directly

        # with open(f'{outputPath}.mp3', 'wb') as audio_out:
        #     audio_out.write(audio_stream)
