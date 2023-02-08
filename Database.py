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
            date_modify text,
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
    