
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User
from utils import save_upload

@app.route("/profile/change-information", methods=["post"])
def profile_change_information():

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    if not (user.seller or user.admin):
        flash("No access")
        return redirect("/profile/information")
    
    short_bio = request.form["short_bio"]
    full_bio = request.form["full_bio"]
    discord = request.form["discord"]
    youtube = request.form["youtube"]
    telegram = request.form["telegram"]

    preview_image1 = save_upload(request.files.get("preview_image1"))
    preview_image2 = save_upload(request.files.get("preview_image2"))
    preview_image3 = save_upload(request.files.get("preview_image3"))

    try:
        user.short_bio = short_bio
        user.full_bio = full_bio
        user.yt_link = youtube
        user.ds_link = discord
        user.tg_link = telegram
        if preview_image1 != "None":
            user.preview_image1 = preview_image1
        if preview_image2 != "None":
            user.preview_image2 = preview_image2
        if preview_image3 != "None":
            user.preview_image3 = preview_image3

        db.session.commit()
        flash("Information successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/information")