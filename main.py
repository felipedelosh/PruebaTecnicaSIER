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

@app.route('/health')
def health():
    app.logger.info("GET the server status.")
    return "Server is OK"


#Start
if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=4000)
