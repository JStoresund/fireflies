# from flask import Flask, render_template
# from flask_socketio import SocketIO, send, emit
# from random import choice

# app=Flask(__name__)
# app.config["SECRET_KEY"]="secret"

# Socket = SocketIO(app)


# @app.route('/')
# def home():
#     return render_template('hjem.tpl', sync_mode=Socket.async_mode)

# #Fargeskjerm. Her må man sendes etter å ha fylt ut info på hjemskjermen 
# @app.route('/farge')
# def colour():
#     colors=["red", "blue", "green", "yellow", "orange", "purple", "pink", "black"]
#     randColor=choice(colors) # Picks random color from colors
#     return render_template('colour.tpl', randColor=randColor, sync_mode=Socket.async_mode)


# @Socket.on("connection")
# def handleMessage():
#     print("Connected")

# @Socket.on("message")
# def handleMessage(msg):
#     print("Message:", msg)
#     send(msg, broadcast=True)

# @app.route("/websocket")
# def socket():
#     return render_template("websocket.html")

# if __name__ == "__main__":
#     Socket.run(app, host="localhost", debug=True, use_reloader=True, port=3000)



from flask import Flask, send_from_directory, send_file
from flask_socketio import SocketIO, emit
from random import choice

app=Flask(__name__)

socketio = SocketIO(app)

colors=["red", "blue", "green", "yellow", "orange", "purple", "pink", "black"]

@app.route('/farge')
def farge():
    return send_file('templates/websocket.html')

@app.route("/")
def home():
    return send_file("templates/hjem.html")

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
@app.route('/static/<path:path>')
def getStataticFile(path):
    return send_from_directory("static", path) 

@socketio.on('update:color')
def handle_message(data):
    emit("update:color", choice(colors), broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True, use_reloader=True, port=8000)