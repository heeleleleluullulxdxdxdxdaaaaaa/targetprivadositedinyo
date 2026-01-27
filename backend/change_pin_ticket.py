
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User, Ticket

@app.route("/profile/pin-ticket/<int:ticket_id>", methods=["get"])
def profile_pin_ticket(ticket_id):

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
        return redirect("/profile/active_tickets")
        
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket:
        flash("Ticket not found in database")
        return redirect("/profile/active_tickets")

    try:
        ticket.pin = not ticket.pin
        db.session.commit()
        flash("Ticket pin status successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/active_tickets")