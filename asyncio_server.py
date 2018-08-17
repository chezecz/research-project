import asyncio

class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        super.__init__()

def run_server(host, port):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(
            ClientServerProtocol,
            host, port
        )

        server = loop.run_until_complete(coro)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == '__main__':
    run_server('127.0.0.1', 8888)