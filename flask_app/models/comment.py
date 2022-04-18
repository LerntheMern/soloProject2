from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment: 
    db = "patients_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.injury = None


    @classmethod
    def add_comment_to_db(cls, data):
        query = "INSERT into comments (comment, injury_id) VALUE(%(comment)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    

    @staticmethod
    def validate_new_comment(form_data):
        is_valid = True
        if len(form_data["comment"]) < 3:
            is_valid = False
            flash("Comment must be at least 3 characters.")
        return is_valid