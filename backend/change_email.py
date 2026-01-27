
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User
from utils import validate_email

@app.route("/profile/change-email", methods=["post"])
def profile_change_email():

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    email = request.form["email"]
    if not email:
        flash("Email field not found")
        return redirect("/profile/general_information")
    
    if not validate_email(email):
        flash("Email invalid")
        return redirect("/profile/general_information")
    
    try:
        user.email = email
        db.session.commit()
        flash("Email successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/general_information")