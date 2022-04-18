from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.injury import Injury

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), all_injuries = Injury.get_all_injuries_with_users())

@app.route("/programs/<int:id>")
def view_injury_page(id):
    if "user_id" not in session:
        return redirect("/")
    injury_data = {
        "id" : id
    }
    data = {
        "id" : session["user_id"]
    }
    return render_template("view_injury.html", this_injury = Injury.get_one_injury_with_user(injury_data), user=User.get_by_id(data))

@app.route('/injury/<int:id>/delete')
def delete_injury(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id 
    }
    Injury.delete_injury(data)
    return redirect("/dashboard")