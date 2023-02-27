from flask import Flask, send_from_directory, send_file
from flask_socketio import SocketIO, emit
from random import choice
import stupidArtnet
from time import sleep




LocalIp = "1.0.0.255"
Target_Universe = 0

listen_server=stupidArtnet.StupidArtnetServer()

def received_data(data):
    print("Received data: \n", data)

u0_listener=listen_server.register_listener(universe=0, callback_function=received_data)

print(listen_server)

sleep(3)

buffer=listen_server.get_buffer(u0_listener)

n_data = len(buffer)
if n_data > 0:
    # in which channel 1 would be
    print('Channel 1: ', buffer[0])

    # and channel 20 would be
    print('Channel 20: ', buffer[19])
    print(buffer)

else:
    print("Didn't find anything")
    print(buffer)

del listen_server









app=Flask(__name__)

socketio = SocketIO(app)

colors=["#FD5B78", "#50BFE6", "#FFCC33", "#FF9933", "#EE34D2", "#66FF66", "#FF6EFF"]

# # Koble opp mot artnet-input

# artnet_input=[0b1011, 0b0101, 0b0001] # ...

# # End

@app.route('/farge')
def farge():
    return send_file('websocket.html')

@app.route("/")
def home():
    return send_file("hjem.html")

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
@app.route('/static/<path:path>')
def getStataticFile(path):
    return send_from_directory("static", path) 

@socketio.on('update:color')
def handle_message(data):
    emit("update:color", choice(colors), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)
