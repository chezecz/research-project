import asyncio
import zlib
import queue
import threading

from google.cloud import speech

from config import Config
from config import Server

buffer = queue.Queue()
buffer_response = queue.Queue()

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
            sample_rate_hertz=Config.rate
        )
        config = speech.types.StreamingRecognitionConfig(config=config, interim_results = True)
        requests = (speech.types.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator)
        results = client.streaming_recognize(config, requests)

        for result in results:
            for data in result.results:
                for parts in data.alternatives:
                    buffer_response.put(parts.transcript)

def activate_job():
    background = threading.Thread(target=get_transcription, args=())
    background.daemon = True
    background.start()

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        buffer.put(zlib.decompress(data), block=False)
        if buffer_response.empty():
            self.transport.sendto("", addr)
        else:
            self.transport.sendto(buffer_response.get(), addr)

def run_server(host, port):
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
    run_server('127.0.0.1', 8888)