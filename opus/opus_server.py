import asyncio
import zlib
import queue
import threading
import audioop

from google.cloud import speech
from opuslib import Decoder

from config.config import Config
from config.config import Server
from config.config import Opus

buffer = queue.Queue()
buffer_response = queue.Queue()

dec = Decoder(Opus.rate, Opus.channels)

def chunks():
    while True:
        try:
            yield buffer.get(timeout = 1)
        except queue.Empty:
            break

def get_transcription():
    while True:
        generator = chunks()
        client = speech.SpeechClient()
        config = speech.types.RecognitionConfig(
            encoding=Config.encoding,
            language_code=Config.language,
            sample_rate_hertz=Opus.rate
        )
        config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)
        requests = (speech.types.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator)
        results = client.streaming_recognize(config, requests)

        for result in results:
            print(result)
            for data in result.results:
                for parts in data.alternatives:
                    buffer_response.put(parts.transcript)

def activate_job():
    background = threading.Thread(target=get_transcription, args=())
    background.daemon = True
    background.start()

class EchoServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = dec.decode(zlib.decompress(data), Opus.chunk)
        buffer.put(message)
        if buffer_response.empty():
            self.transport.sendto(b'', addr)
        else:
            self.transport.sendto(buffer_response.get().encode(), addr)

def run_server():
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(
        EchoServerProtocol, local_addr=(Server.host, Server.port))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()

if __name__ == '__main__':
    activate_job()
    run_server()