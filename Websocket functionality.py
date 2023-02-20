from bottle import route, run, template, static_file
import random

#HUSK!
# % for for-loops of if-statements. Tekst inni {{}} anses som pythonkode

#Hjemskjerm. Her kommer info bruker må fylle ut for å kartlegge mobile enheter. Dvs. felt, rad og setenummer
@route('/')
def home():
    return template('hjem')

@route("/style.css")
def style():
    return template("style.css")

@route("/logo.jpg")
def logo():
    return template("MGPlogo.jpg")

#Fargeskjerm. Her må man sendes etter å ha fylt ut info på hjemskjermen 
@route('/farge')
def colour():
    return template('colour')

#Route for å implementere statiske filer til hjemskjerm. Dvs. MGP-bilde
@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='./views/static') 

run(debug=True, reloader=True)

