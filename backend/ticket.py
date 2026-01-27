
from config import app, socketio, NOWPAYMENTS_BASE_URL, bot
from flask import session, flash, redirect, url_for, render_template, jsonify, request
from database import User, Ticket, db, TicketMessage
from utils import get_avatar_path
from flask_socketio import emit, join_room
import os
import uuid
import json
import requests
from werkzeug.utils import secure_filename

@socketio.on('join_ticket')
def handle_join_ticket(data):
    ticket_id = data['ticket_id']
    join_room(f'ticket_{ticket_id}')

@app.route("/profile/ticket/<int:ticket_id>", methods=["get"])
def profile_ticket(ticket_id):

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if not user.admin:
        if not user_id in [ticket.seller_id, ticket.user_id]:
            flash("No access")
            return redirect("/profile/general_information")
        
    view = "User"
    if user.seller or user.admin:
        view = "Seller"

    ticket_messages = TicketMessage.query.filter_by(ticket_id=ticket_id).all()
        
    return render_template(f'profile/ticket.html', 
                    user_id=user_id,
                    ticket_user_id=ticket.user_id,
                    seller_id=ticket.seller_id,
                    ticket_id=ticket_id,
                    view=view,
                    ticket_messages=ticket_messages,
                    created_at=Ticket.query.filter_by(id=ticket_id).first().created_at)