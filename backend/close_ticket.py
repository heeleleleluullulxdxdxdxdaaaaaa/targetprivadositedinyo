
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User, Product, Ticket, TicketMessage

@app.route("/profile/close-ticket/<string:ticket_id>", methods=["get"])
def profile_close_ticket(ticket_id):

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
            
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket:
        flash("Ticket not found in database")
        return redirect("/profile/active_tickets")
    
    if not user.admin:
        if not user_id in [ticket.seller_id, ticket.user_id]:
            flash("No access")
            return redirect("/profile/active_tickets")
    
    try:
        ticket_messages = TicketMessage.query.filter_by(ticket_id=ticket_id).all()
        for ticket_message in ticket_messages:
            db.session.delete(ticket_message)
        db.session.delete(ticket)
        db.session.commit()
        flash("Ticket successfully closed")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
        
    return redirect("/profile/active_tickets")