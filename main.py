"""
FelipedelosH
2023

Server SIER
"""
from flask import Flask, Response, request, render_template
import logging
from Database import *
from EventController import *

# Declares Database and init
database = Database()

# Declarates a Controller
controller = EventController()

# Generate a Static events
controller.generateStaticEvents()

# Configurates a Logger
logging.basicConfig(filename="logs.log", format="%(levelname)s:%(name)s:%(message)s")

# Declarates a Server APP
app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    context = {
        "error" : error
    }

    userIp = request.remote_addr
    _url = request.base_url
    app.logger.info(f"The user: {userIp} try to find resource: {_url}")

    return render_template('404.html', **context)

@app.errorhandler(405)
def not_found(error):
    context = {
        "error" : error
    }

    userIp = request.remote_addr
    _url = request.base_url
    app.logger.info(f"The user: {userIp} try to access: {_url}")

    return render_template('405.html', **context)

@app.route('/health')
def health():
    userIp = request.remote_addr
    app.logger.info(f"The user: {userIp} ping APP")
    return "Server is OK"

@app.route('/event', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def event():
    userIp = request.remote_addr

    if request.method == 'GET':
        app.logger.info(f"The user: {userIp} get event information")
        params = request.args
        information = controller.getEvents(params)
        return information

    if request.method == 'POST':
        json = request.get_json()
        insert_status = controller.insertEvent(json)
        if insert_status["status"] == 200:
            app.logger.info(f"The user: {userIp} insert envent in database")
        else:
            app.logger.info(f"The user: {userIp} fail to insert envent in database")
        
        return insert_status

    if request.method == 'PATCH':
        json_data = request.get_json()
        edit_status = controller.editEvent(json_data)

        if edit_status["status"] == 200:
            app.logger.info(f"The user: {userIp} edit envent in database")
        else:
            app.logger.info(f"The user: {userIp} fail to edit a envent in database")

        return edit_status

    if request.method == 'DELETE':
        id_in_json = request.get_json()
        delete_event_information = controller.deleteEvent(id_in_json)
        if  delete_event_information["status"] == 200:
            app.logger.info(f"The user: {userIp} delete envent in database")
        else:
            app.logger.info(f"The user: {userIp} try to delete a envent in database")

        return delete_event_information


@app.route('/gestion', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def gestion():
    if request.method == 'GET':
        return("GET")

    if request.method == 'POST':
        json = request.get_json()
        insert_status = controller.insertGestion(json)

        if insert_status["status"] == 200:
            pass
        else:
            pass

        return insert_status

    if request.method == 'DELETE':
        return("DELETE")

    if request.method == 'PATCH':
        return("PATCH")


#Start
if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=4000)
