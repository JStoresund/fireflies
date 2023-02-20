from bottle import route, run, template, static_file, get
from bottle_websocket import GeventWebSocketServer
from bottle_websocket import websocket


#HUSK!
# % for for-loops of if-statements. Tekst inni {{}} anses som pythonkode

#Hjemskjerm. Her kommer info bruker må fylle ut for å kartlegge mobile enheter. Dvs. felt, rad og setenummer
@route('/')
def home():
    return template('hjem.tpl')

@route("/style.css")
def style():
    return template("style.css")

#Fargeskjerm. Her må man sendes etter å ha fylt ut info på hjemskjermen 
@route('/farge')
def colour():
    return template('colour')

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='./views/static') 

@route("/index")
def index():
    return template("index")

@get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive()
        if msg is not None:
            ws.send(msg)
        else: break

run(host='127.0.0.1', reloader=True, port=8000, server=GeventWebSocketServer)

