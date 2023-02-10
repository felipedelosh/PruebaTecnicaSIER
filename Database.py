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
            id integer primary key AUTOINCREMENT,
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
            information = {"status":True, "message":"Count of all Events" ,"data" : cursor.fetchone()[0]}
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
            information = {"status":False, "message":"Error to Search Event information", "data": []}

        self.conection.close()
        return information


    def getHideEvents(self):
        """
        Return all events eliminates
        """
        sql = """
        select * from event where visible = 0
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
                event["date_mod"] = i[5]
                event["status"] = i[6]
                event["visible"] = i[7]
                data.append(event)

            information = {"status":True, "message":"All information of events > total: "+str(len(data)), "data": data}
            cursor.close()
        except:
            information = {"status":False, "message":"Error to Search Event information", "data": []}

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
        insert into event (name_event, type_event, description, date_create, date_last_update, status_event, visible) values (?,?,?,?,?,?,?)
        """
        insert_status = {}
        try:
            self.conection = sqlite3.connect("database.db")
            values = (event_params["name_event"], event_params["type_event"], event_params["description"], event_params["date_event"], event_params["date_event"], event_params["status_event"], 1)
            self.conection.execute(sql, values)
            self.conection.commit()
            insert_status = {"status": True, "message": "Event ID:" + "?" + " insert successfull"}
        except:
            insert_status =  {"status": False, "message": "Error to insert Event"}
    
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


    def editEvent(self, args):
        """
        Construct a SQL query and execute
        """
        #  Return status
        information = {}

        # create a query
        sql = "UPDATE event SET "
        edit_cols_names = []
        data = []

        exists_name_event = "name_event" in args
        exists_type_event = "type_event" in args
        exists_description = "description" in args
        exists_date_event = "date_event" in args
        exists_status_event = "status_event" in args

        if exists_name_event:
            edit_cols_names.append("name_event = ?")
            data.append(args["name_event"])


        if exists_type_event:
            edit_cols_names.append("type_event = ?")
            data.append(args["type_event"])

        if exists_description:
            edit_cols_names.append("description = ?")
            data.append(args["description"])

        if exists_date_event:
            edit_cols_names.append("date_event = ?")
            data.append(args["date_event"])

        if exists_status_event:
            edit_cols_names.append("status_event = ?")
            data.append(args["status_event"])

        for i in edit_cols_names:
            sql = sql + i + ","

        # Erase last comma
        sql = sql[0:len(sql)-1]

        # Add where
        sql = sql + " WHERE ID = ?"
        data.append(int(args["id"]))

        # Create a tuple
        tuple = ()
        for i in data:
            tuple = tuple + (i, )
        # End to create Query


        # Edit ROW
        try:
            self.conection = sqlite3.connect("database.db")
            cursor = self.conection.execute(sql, tuple)
            self.conection.commit()
            cursor.close()
            information = {"status":True, "message":"Edit a Event "+str(args["id"])}
        except:    
            information = {"satus":True, "message": "Not Edit event with id " + str(args["id"])}


        return information


