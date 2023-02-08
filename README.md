# PruebaTecnicaSIER


This is my solution of SIER
![Flask.py](Docs/flask.JPG)


# 0 -> Install dependencies:

python3 -m pip install flask


# 1 -> To Excecute:

Run the main file (main.py) and consume via POSTMAN.

# 2 -> About Database

This is in SQLite3 (For easy implemetation) and consume through file (Database.py)

Event(ID,name_event,type_event,)

ID >> Is a integer to identify a Event.
name_event >> Is a text to put a name of event
type_event >> Is a text to diferenciates a type of event PUT GET DELETE PACTH ...
description >> Is a text to comment a event
date >> Is a timedate of server 
status_event >> only two types PendingRevision | Revisated 
visible >> Integer 1 or 0  to indicates if event is delete or not delete


# 3 -> About the routes

NOT HTTPs only HTTP

## localhost + port + / + endpoint

http://localhost:4000/health

Say if the server is running.



