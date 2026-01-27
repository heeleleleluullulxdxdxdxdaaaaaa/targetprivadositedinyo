
from flask import url_for
from database import User, TicketMessage, Order, Product
import os
from werkzeug.utils import secure_filename
import re
from config import app
import jinja2
import datetime

def validate_email(email):
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email))

def convert_youtube_to_embed(url):

    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([^?]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^?]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)

            video_id = video_id.split('&')[0]
            video_id = video_id.split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
    
    return url

def get_avatar_path(id):

    if not id:
        return url_for('static', filename=f'images/avatar.png')

    user = User.query.filter_by(id=id).first()
    if not user:
        return url_for('static', filename=f'images/avatar.png')
    
    avatar_path = url_for('static', filename=f'uploads/{user.avatar_filename}')
    
    if avatar_path == "/static/uploads/None":
        avatar_path = url_for('static', filename=f'images/avatar.png')

    return avatar_path

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

def get_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return product

def get_product_solds(product_id):
    return len(Order.query.filter_by(product_id=product_id).all())

def get_last_ticket_message(ticket_id):
    message = TicketMessage.query.filter_by(ticket_id=ticket_id).order_by(TicketMessage.id.desc()).all()
    if message:
        return message[0]
    return None

def format_time(date_string):
    """
    Форматирует строку с датой и временем в формат 'ЧЧ:ММ'
    
    Args:
        date_string (str): Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
    
    Returns:
        str: Время в формате 'HH:MM'
    """

    try:
        dt = datetime.datetime.strptime(str(date_string), '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%H:%M')
    except (ValueError, TypeError):
        return "00:00"
    
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            if os.path.exists(file_path):
                values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def object_len(object) -> int:
    if object:
        try:
            obj_len = len(object)
            return obj_len
        except:
            return 0
    return 0

def get_seller_product_count(seller_id):
    return len(Product.query.filter_by(seller_id=seller_id).all())

app.jinja_env.globals.update(get_seller_product_count=get_seller_product_count)
app.jinja_env.globals.update(object_len=object_len)
app.jinja_env.globals.update(get_product_solds=get_product_solds)
app.jinja_env.globals.update(get_avatar_path=get_avatar_path)
app.jinja_env.globals.update(get_user=get_user)
app.jinja_env.globals.update(get_product=get_product)
app.jinja_env.globals.update(get_last_ticket_message=get_last_ticket_message)
app.jinja_env.globals.update(format_time=format_time)
app.jinja_env.globals.update(dated_url_for=dated_url_for)

def save_upload(img) -> str:
    image_filename = None
    if img and img.filename != '':
        filename = secure_filename(img.filename)
        unique_filename = f"{os.urandom(8).hex()}_{filename}"
        filepath = os.path.join(app.config['UPLOADS_FOLDER'], unique_filename)
        img.save(filepath)
        image_filename = unique_filename
    return str(image_filename)

def save_source(source) -> str:
    image_filename = None
    if source and source.filename != '':
        filename = secure_filename(source.filename)
        unique_filename = f"{os.urandom(8).hex()}_{filename}"
        filepath = os.path.join(app.config['SOURCES_FOLDER'], unique_filename)
        source.save(filepath)
        image_filename = unique_filename
    return str(image_filename)