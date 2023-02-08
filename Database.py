"""
FelipedelosH
2023

"""
import sqlite3

class Database:
    def __init__(self) -> None:
        self.conection = sqlite3.connect("database.db")

        self.createsTables()
    
    def createsTables(self):
        sql = """
        create table if not exists Event
        (
            id integer primary key,
            name_event text,
            type_event text,
            description text,
            date_create text,
            date_last_update text,
            status_event text,
            visible integer
        )
        """
        try:
            self.conection = sqlite3.connect("database.db")
            self.conection.execute(sql)
            self.conection.close()
        except:
            print("Error Generate DB")

    def countAllEvents(self):
        """
        Return int with all quantity of events
        """
        sql = """
        select count(*) from event
        """

    def insertEvent(self, event_params):
        """
        Try to insert a event in database

        """
        sql = """
        insert into event (id, name_event, type_event, description, date_create, date_last_update, status_event, visible) values (?,?,?,?,?,?,?,?)
        """
        insert_status = {}
        try:
            self.conection = sqlite3.connect("database.db")
            values = (event_params["id"], event_params["name_event"], event_params["type_event"], event_params["description"], event_params["date_event"], event_params["date_event"], event_params["status_event"], 1)
            self.conection.execute(sql, values)
            self.conection.commit()
            insert_status = {"status": True, "message": "Event ID:" + str(event_params["id"]) + " insert successfull"}
        except:
            insert_status =  {"status": False, "message": "Not insert Event with id"+str(event_params["id"]) + "Duplicated ID?"}
    
        self.conection.close()
        return insert_status
