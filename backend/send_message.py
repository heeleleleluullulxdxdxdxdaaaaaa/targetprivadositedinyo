
from config import socketio
from flask import session
from database import db, User, Ticket, TicketMessage
from flask_socketio import emit
from utils import get_avatar_path, get_last_ticket_message

@socketio.on('send_message')
def handle_send_message(data):
    user_id = session.get("user_id")
    if not user_id:
        return
    
    ticket_id = data['ticket_id']
    message_text = data['message']
    
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if ticket and (user_id in [ticket.user_id, ticket.seller_id] or User.query.get(user_id).admin):
        
        is_continue = False
        if get_last_ticket_message(ticket_id):
            if get_last_ticket_message(ticket_id).user_id == user_id:
                    is_continue = True

        ticket_message = TicketMessage(
            ticket_id=ticket_id,
            user_id=user_id,
            message=message_text,
            is_image=False,
            is_continue=is_continue
        )
        db.session.add(ticket_message)
        db.session.commit()
        
        user = User.query.get(user_id)
        emit('new_message', {
            'ticket_id': ticket_id,
            'message': {
                'username': user.username,
                'status': user.status,
                'avatar_path': get_avatar_path(user_id),
                'created_at': ticket_message.created_at.strftime('%Y-%m-%d %H:%M'),
                'message': message_text,
                'is_continue': is_continue,
                'is_image': False
            }
        }, room=f'ticket_{ticket_id}')

"""@app.route("/profile/ticket/send-message/<int:ticket_id>", methods=["post"])
def profile_ticket_send_message(ticket_id):

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
        return redirect("/profile/general-information")
    
    if not user.admin:
        if not user_id in [ticket.user_id, ticket.seller_id]:
            flash("No access")
            return redirect("/profile/general-information")
        
    message_text = request.form["message_text"]
    if not message_text:
        flash("Message field not found")
        return redirect(f"/profile/ticket/{ ticket_id }")
    
    try:
        ticket_message = TicketMessage(
            ticket_id=ticket_id,
            user_id=user_id,
            message = message_text,
            is_image=False
        )
        db.session.add(ticket_message)
        db.session.commit()
        return redirect(f"/profile/ticket/{ticket.id}")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
        
    return redirect("/profile/general_information")"""