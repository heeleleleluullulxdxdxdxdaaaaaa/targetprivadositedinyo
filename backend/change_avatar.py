from config import app
from flask import request, session, redirect, url_for, flash
import os
from database import User, db
from utils import save_upload

@app.route("/profile/change-avatar", methods=["post"])
def profile_change_avatar():

    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first')
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User not found in database')
        return redirect("/login")
    
    new_avatar = save_upload(request.files.get("file"))
    
    try:
        user.avatar_filename = new_avatar
        db.session.commit()
        flash("Avatar successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
            
    return redirect("/profile/general_information")