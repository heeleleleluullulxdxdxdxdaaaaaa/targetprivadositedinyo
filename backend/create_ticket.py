
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User, Product, Ticket

@app.route("/profile/create-ticket/<string:seller_id>", methods=["get"])
def profile_create_ticket(seller_id):

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
        
    seller = User.query.filter_by(id=seller_id).first()
    if not seller:
        flash("Seller not found in database")
        return redirect("/profile/general_information")
    
    if not (seller.seller or seller.admin):
        flash("This seller have no permisions")
        return redirect("/profile/general_information")
    
    try:
        ticket = Ticket(
            user_id=user_id,
            seller_id=seller_id
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket successfully created")
        return redirect(f"/profile/ticket/{ticket.id}")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
        
    return redirect("/profile/general_information")