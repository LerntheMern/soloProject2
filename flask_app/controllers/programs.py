
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.program import Program
from flask_app.models.injury import Injury

@app.route("/request_program")
def request_new_program():
    if "user_id" not in session:
        return redirect("/")
    return render_template("/request_program.html")

@app.route("/request_program/add", methods = ["POST"])
def add_request():
    if "user_id" not in session:
        return redirect("/")
    if not Program.validate_new_program(request.form):
        return redirect("/request_program")
    data = {
        "injury" : request.form["injury"],
        "cause" : request.form["cause"],
        "location" : request.form["location"],
        "hobbies_activities" : request.form["hobbies_activities"],
        "pain_level" : request.form["pain_level"],
        "user_id" : session["user_id"] 
    }
    Program.request_program(data)
    return redirect("/dashboard")
