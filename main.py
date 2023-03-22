from flask import Flask, send_from_directory, send_file, request, render_template
from flask_socketio import SocketIO
from gevent import monkey
from stupidArtnet import StupidArtnetServer
# import multiprocessing as mp
from time import sleep

monkey.patch_all()

app=Flask(__name__)

socketio = SocketIO(app)

prev_data=[]

connectedUsers={} # Skal mappe socketID-er med setenummer, radnummer og felt
amountOfSeats=2
amountOfRows=10

@app.route('/farge')
def farge():
    return send_file('websocket.html')

@app.route("/")
def home():
    return render_template("hjem.html", amountOfRows=amountOfRows, amountOfSeats=amountOfSeats)

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
@app.route('/static/<path:path>')
def getStaticFile(path):
    return send_from_directory("static", path) 

def getHexString(data):
    return ("#" + 3 * "{:02x}").format(*data)

def posToIndex(rowNumber, seatNumber): # Finn korrekt index i input-listen ut i fra radnummer og setenummer
    return 3*((amountOfRows - rowNumber) * amountOfSeats + seatNumber-1)

@socketio.on('update:color') # Funksjon som kalles når signal kommer fra klient (se websocket.html)
def send_data(data):
    # if prev_data==data:
    #     return
    for user, pos in connectedUsers.items(): # Gå over hver bruker
        try:
            splice = data[posToIndex(pos["rad"], pos["sete"]) : posToIndex(pos["rad"], pos["sete"])+3]
            color=getHexString(splice)
            # print(index)
            socketio.emit("update:color", color)
            print("Sending successful")
        except IndexError:
            print("IndexError: Seat out of range")
        except Exception:
            print(f"Sending failed for user {user} at position {pos}")
    prev_data=data

@socketio.on('build:addUser') # Funksjon som kalles når en ny bruker kobler seg på websocket
def add_user(felt, radNummer, seteNummer):
    print("A user connected to the websocket-server")
    felt=int(felt)
    radNummer=int(radNummer)
    seteNummer=int(seteNummer)
    connectedUsers[ request.sid ] = {"felt": felt, "rad": radNummer, "sete": seteNummer} # Legger bruker inn i dictionary
    print(connectedUsers)

@socketio.on("disconnect")
def remove_user():
    del connectedUsers[ request.sid ]
    print("User removed")

artnet_server=StupidArtnetServer()
listener=artnet_server.register_listener(universe=0, callback_function=send_data)

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