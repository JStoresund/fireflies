from bottle import get, route, run, template
from gevent import monkey
from bottle_websocket import GeventWebSocketServer, websocket
from queue import Queue
from stupidArtnet import StupidArtnetServer

monkey.patch_all()

queue = Queue()
server = StupidArtnetServer()


def channels_to_hexcode(channels):
    assert len(channels) == 3
    return ("#" + 3 * "{:02x}").format(*channels)


def on_artnet_frame(frame):
    queue.put(frame)


listener = server.register_listener(1, callback_function=on_artnet_frame)


@route('/')
def index():
    return template('index.html')


@get('/websocket', apply=[websocket])
def websocket_route(ws):
    while True:
        frame = queue.get()  # Blocks and waits
        ws.send(channels_to_hexcode(frame[0:3]))


run(host='192.168.1.5', port=8080, server=GeventWebSocketServer)
