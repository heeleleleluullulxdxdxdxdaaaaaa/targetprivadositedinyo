
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default="User")
    admin = db.Column(db.Boolean, default=False)
    seller = db.Column(db.Boolean, default=False)
    avatar_filename = db.Column(db.String)
    tg_link = db.Column(db.String)
    ds_link = db.Column(db.String)
    yt_link = db.Column(db.String)
    nowpayments_api_key = db.Column(db.String)
    short_bio = db.Column(db.String)
    full_bio = db.Column(db.Text)
    preview_image1 = db.Column(db.String)
    preview_image2 = db.Column(db.String)
    preview_image3 = db.Column(db.String)
    reg_data = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=False, default="Product")
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String)
    link_to_video = db.Column(db.String, nullable=False)
    image1 = db.Column(db.String, nullable=False)
    image2 = db.Column(db.String)
    image3 = db.Column(db.String)
    pin = db.Column(db.Boolean, default=False)
    in_stock = db.Column(db.Integer, nullable=False, default=-1)
    post_data = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_order_user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', name='fk_order_product_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_order_seller_id'))
    purchase_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Ticket(db.Model):
    __tablename__ = "tickets"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_ticket_user_id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_ticket_seller_id'))
    status = db.Column(db.String, nullable=False, default="active")
    pin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class TicketMessage(db.Model):
    __tablename__ = 'ticket_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id', name='fk_ticket_message_ticket_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_ticket_message_user_id'))
    message = db.Column(db.Text, nullable=False)
    is_continue = db.Column(db.Boolean, default=False)
    is_image = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def init_db():
    with app.app_context():
        db.create_all()
        
init_db()