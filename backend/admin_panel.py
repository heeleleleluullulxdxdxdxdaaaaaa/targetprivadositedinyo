from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, flash
from database import db, User, Product, Order
from config import app

admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

class UserModelView(ModelView):

    column_list = [
        'id', 
        'username', 
        'email', 
        'password', 
        'status', 
        'admin', 
        'seller', 
        'avatar_filename', 
        'tg_link', 
        'ds_link', 
        'yt_link', 
        'nowpayments_api_key', 
        'short_bio', 
        'full_bio', 
        'preview_image1', 
        'preview_image2', 
        'preview_image3',
        'reg_data'
    ]
    
    column_searchable_list = ['username', 'email', 'status']
    column_filters = ['admin', 'seller']
    
    form_columns = [
        'id', 
        'username', 
        'email', 
        'password', 
        'status', 
        'admin', 
        'seller', 
        'avatar_filename', 
        'tg_link', 
        'ds_link', 
        'yt_link', 
        'nowpayments_api_key', 
        'short_bio', 
        'full_bio', 
        'preview_image1', 
        'preview_image2', 
        'preview_image3'
    ]
    
    def is_accessible(self):
        return session.get('admin_access')
    
    def inaccessible_callback(self, name, **kwargs):
        flash('No access', 'error')
        return redirect(url_for('login'))

admin.add_view(UserModelView(User, db.session, name='Users'))

class OrdersModelView(ModelView):

    column_list = ['id', 'user_id', 'product_id', 'seller_id', 'purchase_date']

    column_searchable_list = ['user_id', 'product_id', 'seller_id']
    
    form_columns = ['user_id', 'product_id', 'seller_id']
    
    def is_accessible(self):
        return session.get('admin_access')
    
    def inaccessible_callback(self, name, **kwargs):
        flash('No access', 'error')
        return redirect(url_for('login'))

admin.add_view(OrdersModelView(Order, db.session, name='Orders'))

class ProductModelView(ModelView):

    column_list = ['id', 'seller_id', 'category', 'name', 'price', 'in_stock', 'description', 'filename', 'link_to_video', 'image1', 'image2', 'image3', 'pin', 'post_data']

    column_searchable_list = ['seller_id', 'name']
    
    form_columns = ['seller_id', 'category', 'name', 'price', 'in_stock', 'description', 'filename', 'link_to_video', 'image1', 'image2', 'image3', 'pin']
    
    def is_accessible(self):
        return session.get('admin_access')
    
    def inaccessible_callback(self, name, **kwargs):
        flash('No access', 'error')
        return redirect(url_for('login'))

admin.add_view(ProductModelView(Product, db.session, name='Products'))