import asyncio
import zlib
import queue
import threading
import audioop

from google.cloud import speech

from config.config import Config
from config.config import Server

class VoiceTranscription():
    def __init__(self):
        self.buffer = queue.Queue()
        self.buffer_response = queue.Queue()
        self._clients = set()
        self.activate_job()

    async def new_client(self):
        client = EchoServerProtocol()
        self._client.add(client)

    def put_buffer(self, data):
        self.buffer.put(data)

    def get_buffer(self):
        if self.buffer_response.empty():
            return b''
        else:
            self.buffer_response.get().encode()

    def chunks(self):
        while True:
            try:
                yield self.buffer.get(timeout = 1)
            except queue.Empty:
                break

    def get_transcription(self):
        while True:
            generator = self.chunks()
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
                print(result)
                for data in result.results:
                    for parts in data.alternatives:
                        self.buffer_response.put(parts.transcript)

    def activate_job(self):
        background = threading.Thread(target=self.get_transcription, args=())
        background.daemon = True
        background.start()


class EchoServerProtocol(asyncio.DatagramProtocol):

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = audioop.adpcm2lin(zlib.decompress(data), 2, None)
        buffer = VoiceTranscription()
        buffer.put_buffer(message[0])
        self.transport.sendto(buffer.get_buffer(), addr)


def run_server():
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(
        EchoServerProtocol, local_addr=(Server.host, Server.port))
    transport, protocol = loop.run_until_complete(app.new_client, listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()

if __name__ == '__main__':
    run_server()