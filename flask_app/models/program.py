from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user



class Program:
    db = "patients_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.injury = data["injury"]
        self.cause = data["cause"]
        self.location = data["location"]
        self.hobbies_activities = data["hobbies_activities"]
        self.pain_level = data["pain_level"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.patient = None


    @classmethod
    def request_program(cls,data):
        query = "INSERT into programs (injury, cause, location, hobbies_activities, pain_level, patient_id) VALUE(%(injury)s, %(cause)s, %(location)s, %(hobbies_activities)s , %(pain_level)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_programs_with_users(cls):
        query = "SELECT * FROM programs JOIN patients ON patients.id = programs.patient_id;"
        results = connectToMySQL(cls.db).query_db(query)
        if len(results) < 1:
            return None
        else: 
            all_programs = []
            for each_program in results:
                this_program = cls(each_program)
                this_patient_dictionary = {
                    "id" : each_program["patients.id"],
                    "first_name" : each_program["first_name"],
                    "last_name" : each_program["last_name"],
                    "email" : each_program["email"],
                    "password" : each_program["password"],
                    "created_at" : each_program["patients.created_at"],
                    "updated_at" : each_program["patients.updated_at"]
                }
                program_creator = user.User(this_patient_dictionary)
                this_program.patient = program_creator
                all_programs.append(this_program)
            return  all_programs
    
    @classmethod
    def get_one_program_with_user(cls, data):
        query = "SELECT * FROM programs JOIN patients ON patients.id = programs.patient_id WHERE programs.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return None
        else:
            this_row = results[0]
            one_program = cls(results[0])
            
            this_patient_dictionary = {
                "id" : this_row["patients.id"],
                "first_name" : this_row["first_name"],
                "last_name" : this_row["last_name"],
                "email" : this_row["email"],
                "password" : this_row["password"],
                "created_at" : this_row["patients.created_at"],
                "updated_at" : this_row["patients.updated_at"]
                }
            program_creator = user.User(this_patient_dictionary)
            one_program.patient = program_creator
            return  one_program
    
    @classmethod
    def complete_program(cls,data):
        query = "DELETE FROM injuries WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_new_program(form_data):
        is_valid = True
        if len(form_data["injury"]) < 3:
            is_valid = False
            flash("Injury Name must be at least 3 characters.")
        if len(form_data["cause"]) < 3:
            is_valid = False
            flash("Cause of Injury must be at least 3 characters.")
        if len(form_data["location"]) < 3:
            is_valid = False
            flash("Location of Injury must be at least 3 characters.")
        if len(form_data["hobbies_activities"]) < 3:
            is_valid = False
            flash("Hobbies/Activities must be at least 3 characters.")
        if form_data["pain_level"] == "" or int(form_data["pain_level"]) < 1:
            is_valid = False
            flash("Pain Level must be 1 or more.")
        return is_valid