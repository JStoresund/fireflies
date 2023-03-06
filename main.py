from flask import Flask, send_from_directory, send_file
from flask_socketio import SocketIO, emit
from random import choice
import multiprocessing
import stupidArtnet
from time import sleep




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

def received_data(data):
    print("Received data: \n", data)

def motta_info_fra_Per():
    listen_server=stupidArtnet.StupidArtnetServer()

    u0_listener=listen_server.register_listener(universe=1, callback_function=received_data)

    # print(listen_server)
    buffer=listen_server.get_buffer(u0_listener)

    while True:
        print(buffer)
        sleep(0.5)

    del listen_server

def run_server():
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)

if __name__ == "__main__":
    p1=multiprocessing.Process(target=run_server)
    p2=multiprocessing.Process(target=motta_info_fra_Per)

    p1.start()
    p2.start()
