from flask import Flask, send_from_directory, send_file, request
from flask_socketio import SocketIO, emit
from gevent import monkey
import stupidArtnet

monkey.patch_all()

app=Flask(__name__)

socketio = SocketIO(app)

# artnet_data = Queue() # Queue som skal fylles opp med data fra pi fortløpende

def sendToServer():
    send_data(artnet_server.get_buffer())

artnet_server=stupidArtnet.StupidArtnetServer()
listener=artnet_server.register_listener(universe=1, callback_function=sendToServer)

connectedUsers = {} # Skal mappe socketID-er med setenummer, radnummer og felt
amountOfRows=0
amountOfColumns=0

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

@socketio.on('update:color') # Funksjon som kalles når signal kommer fra klient (se websocket.html)
def send_data(data):
    for position, user in connectedUsers:
        try:
            index = data[3((amountOfRows - position[1]) * amountOfRows + position[2]-1) : 3((amountOfRows - position[1]) * amountOfRows + position[2])]
            emit("update:color", getHexString(index), room=user)
            print(index)
        except Exception:
            pass


# def Wave(waveColor, defaultColor, speed):
#     for column in range(1, antallSeter+1):
#         for user, position in connectedUsers:
#             if position[2]==column:
#                 emit("update:color", waveColor, room=user)
#             else:
#                 emit("update:color", defaultColor, room=user)
#         sleep(500/speed)



@socketio.on('build:addUser') # Funksjon som kalles når en ny bruker kobler seg på websocket
def add_user(felt, radNummer, seteNummer):
    print("A user connected to the websocket-server")
    connectedUsers[ (int(felt), int(radNummer), int(seteNummer)) ] = request.sid # Legger bruker inn i dictionary
    amountOfRows=max(amountOfRows, radNummer)
    amountOfColumns=max(amountOfColumns, seteNummer)
    print(connectedUsers)

@socketio.on("remove:removeUser")
def remove_user(felt, radNummer, seteNummer):
    del connectedUsers[ (int(felt), int(radNummer), int(seteNummer)) ]
    print("User removed") #FUNKER IKKE

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)
