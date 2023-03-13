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

newData = Queue()

def addToQueue(frame):
    newData.put(frame)

listen_server=stupidArtnet.StupidArtnetServer()
u0_listener=listen_server.register_listener(universe=1, callback_function=addToQueue)

colors=["#fd5b78", "#50bfe6", "#ffcc33", "#ff9933", "#ee34d2", "#66ff66", "#ff6eff"]



connectedUsers = {} # Skal mappe socketID-er med setenummer, radnummer og felt

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




def receiveData(): # Funksjon som skal motta data fra raspberry. Returnerer en farge
    buffer=newData.get()
    print(buffer)
    if len(buffer)==0:
        # Får ikke signal fra pi => tilfeldig farge
        farge=random.choice(colors)
    else:
        # Får signal fra pi => farge fra lysbord (for øyeblikket satt til svart)
        farge = ("#" + 3 * "{:02x}").format(*buffer)
    return farge


@socketio.on('update:color') # Funksjon som kalles når signal kommer fra klient (se websocket.html)
def handle_message(data):
    emit("update:color", receiveData(), broadcast=True)


@socketio.on('message') # Funksjon som kalles når en ny bruker kobler seg på websocket
def add_user(felt, radNummer, seteNummer):
    print("A user connected to the websocket-server")
    connectedUsers[request.sid] = [felt, radNummer, seteNummer] # Fyll opp med radnummer, setenummer, felt
    print(connectedUsers)

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)
