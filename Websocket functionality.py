from flask import Flask, render_template
from flask_socketio import SocketIO, send
from random import choice

async_mode=None
app=Flask(__name__)
app.config["SECRET_KEY"]="secret"

Socket = SocketIO(app)


@app.route('/')
def home():
    return render_template('hjem.tpl', sync_mode=Socket.async_mode)

#Fargeskjerm. Her må man sendes etter å ha fylt ut info på hjemskjermen 
@app.route('/farge')
def colour():
    colors=["red", "blue", "green", "yellow", "orange", "purple", "pink", "black"]
    randColor=choice(colors) # Picks random color from colors
    return render_template('colour.tpl', randColor=randColor, sync_mode=Socket.async_mode)

@Socket.on("message")
def handleMessage(msg):
    print("Message:", msg)
    send(msg, broadcast=True)

# @app.route("/websocket")
# def socket():
#     return render_template("websocket.html")

if __name__ == "__main__":
    Socket.run(app, host="localhost", debug=True, use_reloader=True)

