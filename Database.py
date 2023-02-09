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
        Return int with all quantity of events in dic
        {status: bool, message: str, data: obj}
        """
        sql = """
        select count(*) from event
        """
        information = {}

        try:
            self.conection = sqlite3.connect("database.db")
            cursor = self.conection.execute(sql)
            information = {"status":True, "message":"Count of all Events" ,"data" : str(cursor.fetchone()[0])}
            cursor.close()
        except:
            information = {"status":False, "message":"Error to Search Event information", "data": []}

        self.conection.close()
        return information

    def getMinimalInformationOfAllEvents(self):
        """
        Return Only the information for the users view
        """
        sql = """
        select id,name_event,type_event,description,date_create,status_event from event where visible = 1
        """
        information = {}
        data = []

        try:
            self.conection = sqlite3.connect("database.db")
            cursor = self.conection.execute(sql)

            for i in cursor:
                event = {}
                event["id"] = i[0]
                event["name"] = i[1]
                event["type"] = i[2]
                event["description"] = i[3]
                event["date"] = i[4]
                event["status"] = i[5]
                data.append(event)

            information = {"status":True, "message":"All information of events > total: "+str(len(data)), "data": data}
            cursor.close()
        except:
            information = {"status":False, "message":"Error to Serach Event information", "data": []}

        self.conection.close()
        return information

    def getEventByID(self, id):
        """
        Return single Event
        {status:bool, message: str, data: Event}
        """
        information = {}
        data = []
        sql = """
        select id,name_event,type_event,description,date_create,status_event from event where visible = 1 and id = ?
        """
        try:
            self.conection = sqlite3.connect("database.db")
            cursor = self.conection.execute(sql, (id, ))

            row = cursor.fetchone()
            event = {}
            event["id"] = row[0]
            event["name"] = row[1]
            event["type"] = row[2]
            event["description"] = row[3]
            event["date"] = row[4]
            event["status"] = row[5]
            data.append(event)


            information = {"status":True, "message": "Event Nr "+str(id), "data": data}
            cursor.close()
        except:
            information = {"status":False, "message": "Not get Event Nr "+str(id), "data": data}

        self.conection.close()
        return information


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

    def deleteEvent(self, id):
        """
        Hide a event in database
        """
        sql = """
        UPDATE event SET visible = 0 where id = ?
        """
        information = {}
        try:
            self.conection = sqlite3.connect("database.db")
            cursor = self.conection.execute(sql, (id, ))
            self.conection.commit()
            cursor.close()
            information = {"status":True, "message":"Delete a Event "+str(id)}
        except:
            information = {"status":False, "message":"Not delete a Event with id ="+str(id)}

        self.conection.close()
        return information
