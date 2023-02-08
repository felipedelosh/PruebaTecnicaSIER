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

        params_status = self.validatesEventInputParams(event_model_params)
        if params_status["status"]:
            # Insert the event and get the status
            insert_status = self.dbConector.insertEvent(event_model_params)

            if insert_status["status"]:
                return {"status": 202, "mesagge": insert_status["message"]}
            else:
                return {"status": 402, "mesagge": insert_status["message"]}

        else:
            return {"status": 401, "mesagge": params_status["mesagge"]}


        

    def validatesEventInputParams(self, eventParams):
        """
        validates if all insert params of event are ok
        return {status: bool, message: str}
        """
        message = ""
        errors_counter = 0

        if "id" not in eventParams:
            message = message + "Not found 'id', "
            errors_counter = errors_counter + 1
        else:
            try:
                if int(eventParams["id"]) < 0:
                    message = message + "Not insert negative 'id', "
                    errors_counter = errors_counter + 1
            except:
                message = message + "Not valid 'id', "
                errors_counter = errors_counter + 1

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

        if errors_counter == 0:
            return {"status": True}
        else:
            message = message + " Total errors: "+str(errors_counter)
            return {"status": False, "mesagge": message}

