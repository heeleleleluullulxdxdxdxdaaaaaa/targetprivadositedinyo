
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User

@app.route("/profile/change-username", methods=["post"])
def profile_change_username():

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    username = request.form["username"]
    if not username:
        flash("Username field not found")
        return redirect("/profile/general_information")
    
    if len(username) < 4:
        flash("Minimal username lenght is 4")
        return redirect("/profile/general_information")
    
    if len(username) > 20:
        flash("Maximal username lenght is 20")
        return redirect("/profile/general_information")
        
    try:
        user.username = username
        db.session.commit()
        flash("Username successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/general_information")