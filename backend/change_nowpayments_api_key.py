
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User

@app.route("/profile/change-nowpayments-api-key", methods=["post"])
def profile_change_nowpayments_api_key():

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
        return redirect("/profile/payment_details")
    
    nowpayments_api_key = request.form["nowpayments_api_key"]
    password = request.form["password"]
    if not nowpayments_api_key or not password:
        flash("Fields not found")
        return redirect("/profile/payment_details")
    
    if password != user.password:
        flash("Invalid password")
        return redirect("/profile/payment_details")
        
    try:
        user.nowpayments_api_key = nowpayments_api_key
        db.session.commit()
        flash("Nowpayments api key successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/payment_details")