"""
FelipdelosH
2023
"""
from EventModel import *
from Database import *

class EventController:
    def __init__(self) -> None:
        self.dbConector = Database()

    def insertEvent(self, event_model_params):
        """
        Insert a event
        """

        params_status = self.validatesEventInputParamsToNewEvent(event_model_params)

        if params_status["status"]:
            # Insert the event and get the status
            insert_status = self.dbConector.insertEvent(event_model_params)

            if insert_status["status"]:
                return {"status": 200, "message": insert_status["message"]}
            else:
                return {"status": 402, "message": insert_status["message"]}
    
        else:
            return {"status": 401, "message": params_status["message"]}


    def getEvents(self, filters):
        """
        return information about event with the filers
        """
        information = {}

        filter_id ="id" in filters

        if filter_id:

            if filters["id"] == "all":
                all_events = self.dbConector.getMinimalInformationOfAllEvents()
                if all_events["status"]:
                    information =  {"status":200, "message": all_events["message"], "data": all_events["data"]}
                else:
                    information =  {"status":401, "message": all_events["message"], "data": all_events["data"]}
            
            elif filters["id"] == "count":
                event_count = self.dbConector.countAllEvents()
                if event_count["status"]:
                    information = {"status":200, "message": event_count["message"], "data": event_count["data"]}
                else:
                    information = {"status":401, "message": event_count["message"], "data": event_count["data"]}
            elif filters["id"] == "delete" or filters["id"] == "hide":
                delete_events = self.dbConector.getHideEvents()
                if delete_events["status"]:
                    information = {"status":200, "message": delete_events["message"], "data": delete_events["data"]}
                else:
                    information = {"status":401, "message": delete_events["message"], "data": delete_events["data"]}
            else:
                # Get indidual resouce?
                try:
                    id = int(filters["id"])
                    get_event_information = self.dbConector.getEventByID(id)
                    if get_event_information["status"]:
                        information = {"status":200, "message": get_event_information["message"], "data": get_event_information["data"]}
                    else:
                        information = {"status":401, "message": get_event_information["message"], "data": get_event_information["data"]}

                except:
                    information = {"status":401, "message": "not processed solicitude", "data": []}

        return information
        

    def validatesEventInputParamsToNewEvent(self, eventParams):
        """
        validates if all insert params of new event are ok
        return {status: bool, message: str}
        """
        message = ""
        errors_counter = 0

        if "name_event" not in eventParams:
            message = message + "Not found 'name_event', "
            errors_counter = errors_counter + 1

        if "type_event" not in eventParams:
            message = message + "Not found 'name_event', "
            errors_counter = errors_counter + 1

        if "description" not in eventParams:
            message = message + "Not found 'description', "
            errors_counter = errors_counter + 1

        if "date_event" not in eventParams:
            message = message + "Not found 'date_event', "
            errors_counter = errors_counter + 1

        if "status_event" not in eventParams:
            message = message + "Not found 'status_event', "
            errors_counter = errors_counter + 1
        else:
            if eventParams["status_event"] != "PendingRevision":
                message = message + "Error in 'status_event' always 'PendingRevision' for new events, "
                errors_counter = errors_counter + 1

        if errors_counter == 0:
            return {"status": True, "message": "All OK"}
        else:
            message = message + " Total errors: "+str(errors_counter)
            return {"status": False, "message": message}

    def validatesEventInputParamsToEditEvent(self, args):
        """
        Validates if the params in args are ok to edit a event
        return {status:bool, message: str}
        """
        message = ""
        errors_counter = 0

        id_satus = self._validatesEventID(args)
        if not id_satus["status"]:
            errors_counter = errors_counter + 1
            message = id_satus["message"]

        hav_status_event = "status_event" in args
        if hav_status_event:
            if not self._validatesIfEventStatusIsOk(args):
                errors_counter = errors_counter + 1
                message =  message + "Invalid State Event in params, "

        # Indicates a params to edit?
        if not ("name_event" in args or "type_event" in args or "description" in args or "date_event" in args or "status_event" in args):
            errors_counter = errors_counter + 1
            message = "Not indicates a event input params"

        if errors_counter == 0:
            return {"status": True, "message": "All OK"}
        else:
            return {"status": False, "message": message}

    def _validatesEventID(self, args):
        """
        Enter a json with all Event params
        and return if id is ok
        return {status: bool, message: str}
        """

        if "id" not in args:
            return {"status": False, "message": "Not found 'id', "}
        else:
            try:
                if int(args["id"]) < 0:
                    return {"status": False, "message": "Not insert negative 'id', "}
                else:
                    return {"status": True, "message": ""}
            except:
                return {"status": False, "message": "Not valid 'id', "}

    def _validatesIfEventStatusIsOk(self, args):
        """
        Enter a json with all Event params with status_event
        if return if status_event is ok
        """
        return args["status_event"] == "PendingRevision" or args["status_event"] == "Revised"


    def deleteEvent(self, id_in_json):
        """
        This not erase of database only hide
        return {status:bool, message:str}
        """
        information = {}

        hav_id = "id" in id_in_json

        if hav_id:
            try:
                id = int(id_in_json["id"])
                event_delete_information = self.dbConector.deleteEvent(id)
                if event_delete_information["status"]:
                    information = {"status": 200, "message":event_delete_information["message"]}
                else:
                    information = {"status": 401, "message":event_delete_information["message"]}
            except:
                information = {"status": 401, "message": "Invalid to proccessed 'id'"}
        else:
            information = {"status": 401, "message": "to delete a event you need a 'id'"}

        return information

    def editEvent(self, event_model_params):
        """
        Edit the params indicates en json
        """
        params_status = self.validatesEventInputParamsToEditEvent(event_model_params)

        if params_status["status"]:
            edit_satus = self.dbConector.editEvent(event_model_params)
            return {"status": 200, "message": edit_satus["message"] }
        else:
            return {"status": 401, "message" : params_status["message"]}


    def insertGestion(self, json):
        """
        if json is ok insert a gestion of event in db
        """
        params_status = self._validatesGestionsArgs(json)

        if params_status["status"]:
            insert_status = self.dbConector.insertTypeOfGestionEvent(json)

            if insert_status["status"]:
                return {"status": 200, "message": insert_status["message"]}
            else:
                return {"status": 401, "message": insert_status["message"]}

        else:
            return {"status": 401, "message": params_status["message"]}


    def _validatesGestionsArgs(self, json):
        """
        Return if Json of gestion status is ok
        """

        hav_name = "type_event" in json

        if hav_name:
            if str(json["type_event"]).strip() != "" and isinstance(json["type_event"], str):
                return {"status":True, "message":"Ok"}
            else:
                return {"status":False, "message":"Not valid type of type_event"}
        else:
            return {"status":False, "message":"Need specificates a type_event"}

    def getGestions(self, args):
        """
        return a gestion event informat
        """
        information = {}

        filter_id = "id" in args

        if filter_id:
            if args["id"] == "all":
                all_gestion_event = self.dbConector.getAllTypeOfGestionEvent()
                if all_gestion_event["status"]:
                    information = {"status":200, "message": all_gestion_event["message"], "data": all_gestion_event["data"]}
                else:
                    information = {"status":401, "message": all_gestion_event["message"], "data": all_gestion_event["data"]}

        return information
 

    def generateStaticEvents(self):
        """
        Only if database is empty insert it
        """
        count_rows_db_info = self.dbConector.countAllEvents()
        if count_rows_db_info["status"]:
            if count_rows_db_info["data"] == 0:
                data = []
                e0 = {"name_event" : "evento 1","type_event" : "clase A","description" : "Defecto","date_event" : "09-02-2023","status_event" : "PendingRevision"}
                data.append(e0)
                e1 = {"name_event" : "evento 2","type_event" : "clase A","description" : "Defecto","date_event" : "09-02-2023","status_event" : "PendingRevision"}
                data.append(e1)
                e2 = {"name_event" : "evento 3","type_event" : "clase B","description" : "Defecto","date_event" : "09-02-2023","status_event" : "PendingRevision"}
                data.append(e2)
                e3 = {"name_event" : "evento 4","type_event" : "clase B","description" : "Defecto","date_event" : "09-02-2023","status_event" : "PendingRevision"}
                data.append(e3)
                e4 = {"name_event" : "evento 5","type_event" : "clase C","description" : "Defecto","date_event" : "09-02-2023","status_event" : "PendingRevision"}
                data.append(e4)
                e5 = {"name_event" : "evento 6","type_event" : "clase D","description" : "Defecto","date_event" : "09-02-2023","status_event" : "PendingRevision"}
                data.append(e5)

                for i in data:
                    self.insertEvent(i)

