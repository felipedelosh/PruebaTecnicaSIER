"""
FelipedelosH
2023

Server SIER
"""
from flask import Flask, Response, request, render_template
import logging
from Database import *


# Configurates a Logger
logging.basicConfig(filename="logs.log", format="%(levelname)s:%(name)s:%(message)s")

# Declarates a Server APP
app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    context = {
        "error" : error
    }

    return render_template('404.html', **context)

@app.errorhandler(405)
def not_found(error):
    context = {
        "error" : error
    }

    return render_template('405.html', **context)

@app.route('/health')
def health():
    app.logger.info("GET the server status.")
    return "Server is OK"

@app.route('/event', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def event():
    if request.method == 'GET':
        return ("Estoy GET")

    if request.method == 'POST':
        return ("Estoy POST")

    if request.method == 'PATCH':
        return ("Estoy PACTH")

    if request.method == 'DELETE':
        return ("Estoy DELETE")

    return "Epaaaaaa"
    
    


#Start
if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=4000)
