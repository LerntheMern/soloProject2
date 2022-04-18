from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Injury:
    db = "patients_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.exercises = data["exercises"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.patient = None


    @classmethod
    def get_all_injuries_with_users(cls):
        query = "SELECT * FROM injuries JOIN patients ON patients.id = injuries.patient_id;"
        results = connectToMySQL(cls.db).query_db(query)
        if len(results) < 1:
            return None
        else: 
            all_injuries = []
            for each_injury in results:
                this_injury = cls(each_injury)
                this_patient_dictionary = {
                    "id" : each_injury["patients.id"],
                    "first_name" : each_injury["first_name"],
                    "last_name" : each_injury["last_name"],
                    "email" : each_injury["email"],
                    "password" : each_injury["password"],
                    "created_at" : each_injury["patients.created_at"],
                    "updated_at" : each_injury["patients.updated_at"]
                    }
                injury_creator = user.User(this_patient_dictionary)
                this_injury.patient = injury_creator
                all_injuries.append(this_injury)
            return  all_injuries

    @classmethod
    def get_one_injury_with_user(cls, data):
        query = "SELECT * FROM injuries JOIN patients ON patients.id = injuries.patient_id WHERE injuries.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return None
        else:
            this_row = results[0]
            one_injury = cls(results[0])
            
            this_patient_dictionary = {
                "id" : this_row["patients.id"],
                "first_name" : this_row["first_name"],
                "last_name" : this_row["last_name"],
                "email" : this_row["email"],
                "password" : this_row["password"],
                "created_at" : this_row["patients.created_at"],
                "updated_at" : this_row["patients.updated_at"]
                }
            injury_creator = user.User(this_patient_dictionary)
            one_injury.patient = injury_creator
            return  one_injury
    @classmethod
    def delete_injury(cls,data):
        query = "DELETE FROM injuries WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
