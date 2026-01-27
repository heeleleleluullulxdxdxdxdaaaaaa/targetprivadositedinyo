
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User

@app.route("/profile/change-password", methods=["post"])
def profile_change_password():

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    if not current_password or not new_password:
        flash("Fields not found")
        return redirect("/profile/general_information")
    
    if current_password != user.password:
        flash("Invalid current password")
        return redirect("/profile/general_information")
    
    if len(new_password) < 8:
        flash("Minimal password lenght is 8")
        return redirect("/profile/general_information")
    
    if len(new_password) > 100:
        flash("Maximal password lenght is 100")
        return redirect("/profile/general_information")
        
    try:
        user.password = new_password
        db.session.commit()
        flash("Password successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/general_information")