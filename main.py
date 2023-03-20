from flask import Flask, send_from_directory, send_file, request
from flask_socketio import SocketIO, emit
from gevent import monkey
import stupidArtnet
# import multiprocessing as mp
from time import sleep

monkey.patch_all()

app=Flask(__name__)

socketio = SocketIO(app)

# artnet_data = Queue() # Queue som skal fylles opp med data fra pi fortløpende

previousSignal=[]

def sendToServer(data):
    if (buffer:=artnet_server.get_buffer()) != previousSignal:
        send_data(artnet_server.get_buffer())
    previousSignal=buffer

artnet_server=stupidArtnet.StupidArtnetServer()
listener=artnet_server.register_listener(universe=1, callback_function=sendToServer)

connectedUsers = {} # Skal mappe socketID-er med setenummer, radnummer og felt
amountOfColumns=2
amountOfRows=10

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

def getHexString(data):
    return ("#" + 3 * "{:02x}").format(*data)

def posToIndex(rowNumber, seatNumber):
    return 3*((amountOfRows - rowNumber) * amountOfColumns + seatNumber-1)


@socketio.on('update:color') # Funksjon som kalles når signal kommer fra klient (se websocket.html)
def send_data(data):
    print("2. send_data() called")
    for user, pos in connectedUsers.items():
        try:
            index = data[posToIndex(pos["rad"], pos["sete"]) : posToIndex(pos["rad"], pos["sete"])+3]
            print(f"3. Trying to send color {(color:=getHexString(index))}")
            emit("update:color", color, room=user)
            
            print("4. Sending successful")
        except Exception:
            print(f"Sending failed for user {user} at position {pos}")

@socketio.on('build:addUser') # Funksjon som kalles når en ny bruker kobler seg på websocket
def add_user(felt, radNummer, seteNummer):
    print("A user connected to the websocket-server")
    felt=int(felt)
    radNummer=int(radNummer)
    seteNummer=int(seteNummer)
    connectedUsers[ request.sid ] = {"felt": felt, "rad": radNummer, "sete": seteNummer} # Legger bruker inn i dictionary

    # global amountOfRows
    # global amountOfColumns
    # amountOfRows=max(amountOfRows, radNummer)
    # amountOfColumns=max(amountOfColumns, seteNummer)
    print(connectedUsers)

# TEST
@socketio.on("conn")
def send_init():
    print("1. User connected")
    send_data([0,0,0, 128,128,128, 255,255,255])
# TEST END

@socketio.on("disconnect")
def remove_user():
    del connectedUsers[ request.sid ]
    print("User removed")
    print(connectedUsers)

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)



# def Wave(waveColor, defaultColor, speed):
#     for column in range(1, antallSeter+1):
#         for user, position in connectedUsers:
#             if position[2]==column:
#                 emit("update:color", waveColor, room=user)
#             else:
#                 emit("update:color", defaultColor, room=user)
#         sleep(500/speed)


# def receiveData(): # Funksjon som skal motta data fra raspberry. Returnerer en fargeverdi
#     buffer=artnet_data.get()
#     # print(buffer)
#     if len(buffer)==0:
#         # Får ikke signal fra pi => tilfeldig farge
#         data=""
#     else:
#         # Får signal fra pi => farge fra lysbord (for øyeblikket satt til svart)
#         data = ("#" + 3 * "{:02x}").format(*buffer)
#     return data