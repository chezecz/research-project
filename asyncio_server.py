# Google API Key
# export GOOGLE_APPLICATION_CREDENTIALS=/Users/cheze/python-XXXXXXXXXXXX.json

import asyncio
import zlib
import audioop

from google.cloud import speech

from config import Config
from config import Server

buffer = asyncio.Queue()
response = asyncio.Queue()

def chunks():
    while True:
        if buffer.empty():
            pass
        else:
            yield buffer.get()

async def get_transcription():
    generator = chunks()
    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=Config.encoding,
        language_code=Config.language,
        sample_rate_hertz=Config.rate
    )
    config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)
    requests = await (speech.types.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator)
    results = client.streaming_recognize(config, requests)

    for result in results:
        print(result)
        for data in result.results:
            for parts in data.alternatives:
                response.put(parts.transcript)

class ServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        buffer.put_nowait(audioop.adpcm2lin(zlib.decompress(data), 2, None))
        if response.empty():
            self.transport.sendto(b'', addr)
        else:
            self.transport.sendto(response.get().encode(), addr)


async def run_server():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
       lambda: ServerProtocol(), 
       local_addr=(Server.host, Server.port))

    try:
        await asyncio.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        transport.close()

asyncio.run(run_server())