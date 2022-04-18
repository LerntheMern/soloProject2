from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.injury import Injury
from flask_app.models.comment import Comment


@app.route("/comment/<int:id>")
def make_comment_page(id):
    if "user_id" not in session:
        return redirect("/")
    injury_data = {
        "id" : id
    }
    return render_template("comment.html", this_injury = Injury.get_one_injury_with_user(injury_data))

@app.route("/comment/add/<int:id>", methods = ["POST"])
def add_comment(id):
    if "user_id" not in session:
        return redirect("/")
    if not Comment.validate_new_comment(request.form):
        return redirect(f"/comment/{id}") 
    data = {
        "comment" : request.form["comment"],
        "user_id" : session["user_id"] 
    }
    Comment.add_comment_to_db(data)
    return redirect("/dashboard")