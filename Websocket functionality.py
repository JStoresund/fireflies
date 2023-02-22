# from bottle import route, run, template, static_file, get
# from bottle_websocket import GeventWebSocketServer, websocket
from flask import Flask, render_template
from flask_socketio import SocketIO
import random

async_mode=None
app=Flask(__name__)

Socket = SocketIO(app, async_mode=async_mode)


@app.route('/')
def home():
    return render_template('hjem.tpl', sync_mode=Socket.async_mode)

@app.route("/style.css")
def style():
    return render_template("style.css", sync_mode=Socket.async_mode)

#Fargeskjerm. Her må man sendes etter å ha fylt ut info på hjemskjermen 
@app.route('/farge')
def colour():
    colors=["red", "blue", "green", "yellow", "orange", "purple", "pink", "black"]
    randColor=random.choice(colors)
    return render_template('colour.tpl', randColor=randColor, sync_mode=Socket.async_mode)

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
# @app.route('/static/<filename>', sync_mode=Socket.async_mode)
# def static(filename):
#     return static_file(filename, root='./views/static') 

@app.route("/index")
def index():
    return render_template("index", sync_mode=Socket.async_mode)

# @app.get('/websocket', apply=[websocket])
# def echo(ws):
#     while True:
#         msg = ws.receive()
#         if msg is not None:
#             ws.send(msg)
#         else: 
#             print("WebSocket lukket")
#             break

# run(host='127.0.0.1', reloader=True, port=8000, server=GeventWebSocketServer)

if __name__ == "__main__":
    Socket.run(app, host="localhost", debug=True, use_reloader=True, port=8000)

