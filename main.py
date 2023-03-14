from flask import Flask, send_from_directory, send_file, request
from flask_socketio import SocketIO, emit
from gevent import monkey
import random
import stupidArtnet
from time import sleep
from queue import Queue

monkey.patch_all()

app=Flask(__name__)

socketio = SocketIO(app)

artnet_data = Queue() # Queue som skal fylles opp med data fra pi fortløpende

def addToQueue():
    artnet_data.put(listen_server.get_buffer())

listen_server=stupidArtnet.StupidArtnetServer()
u0_listener=listen_server.register_listener(universe=1, callback_function=addToQueue)

colors=["#fd5b78", "#50bfe6", "#ffcc33", "#ff9933", "#ee34d2", "#66ff66", "#ff6eff"]



connectedUsers = {} # Skal mappe socketID-er med setenummer, radnummer og felt
antallSeter=0

@app.route('/farge')
def farge():
    return send_file('websocket.html')

@app.route("/")
def home():
    return send_file("hjem.html")

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
@app.route('/static/<path:path>')
def getStaticFile(path):
    return send_from_directory("static", path) 


def receiveData(): # Funksjon som skal motta data fra raspberry. Returnerer en fargeverdi
    buffer=artnet_data.get()
    print(buffer)
    if len(buffer)==0:
        # Får ikke signal fra pi => tilfeldig farge
        data=random.choice(colors)
    else:
        # Får signal fra pi => farge fra lysbord (for øyeblikket satt til svart)
        data = ("#" + 3 * "{:02x}").format(*buffer)
    return data

@socketio.on('update:color') # Funksjon som kalles når signal kommer fra klient (se websocket.html)
def handle_message(data):
    emit("update:color", receiveData(), broadcast=True)


def Wave(waveColor, defaultColor, speed):
    for column in range(1, antallSeter+1):
        for position, user in connectedUsers:
            if position[2]==column:
                emit("update:color", waveColor, room=user)
            else:
                emit("update:color", defaultColor, room=user)
        sleep(500/speed)



@socketio.on('build:addUser') # Funksjon som kalles når en ny bruker kobler seg på websocket
def add_user(felt, radNummer, seteNummer):
    print("A user connected to the websocket-server")
    connectedUsers[ (felt, radNummer, seteNummer) ] = request.sid # Legger bruker inn i dictionary
    global antallSeter
    antallSeter=max(antallSeter, int(seteNummer))
    print(connectedUsers)

@socketio.on("remove:removeUser")
def remove_user(felt, radNummer, seteNummer):
    del connectedUsers[ (felt, radNummer, seteNummer) ]
    print("User removed") #FUNKER IKKE

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)
