
from config import socketio, app
from flask import session, jsonify, request
from database import db, User, Ticket, TicketMessage
from flask_socketio import emit
from utils import get_avatar_path, get_last_ticket_message, save_upload

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({'success': False, 'error': 'Please login first'})
        
        ticket_id = request.form.get('ticket_id')
        file = request.files.get('file')
        
        if not file:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        # Сохраняем файл и получаем путь
        file_path = save_upload(file)  # ваша функция сохранения файла
        
        if file_path == "None":
            return jsonify({'success': False, 'error': 'Failed to save file'})
        
        return jsonify({
            'success': True, 
            'file_path': file_path
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@socketio.on('send_image')
def handle_send_image(data):
    user_id = session.get("user_id")
    if not user_id:
        return
    
    ticket_id = data['ticket_id']
    image_path = data['image_path']
    
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    if ticket and (user_id in [ticket.user_id, ticket.seller_id] or User.query.get(user_id).admin):
        
        is_continue = False
        if get_last_ticket_message(ticket_id):
            if get_last_ticket_message(ticket_id).user_id == user_id:
                is_continue = True

        ticket_message = TicketMessage(
            ticket_id=ticket_id,
            user_id=user_id,
            message=image_path,  # путь к изображению
            is_image=True,
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
                'message': image_path,
                'is_continue': is_continue,
                'is_image': True
            }
        }, room=f'ticket_{ticket_id}')