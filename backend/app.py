
from config import app, socketio
import admin_panel
import change_avatar
import change_email
import change_username
import change_password
import change_nowpayments_api_key
import change_information
import download_product
import create_product
import delete_product
import change_product
import change_product_pin
import create_ticket
import send_message
import change_pin_ticket
import close_ticket
import delete_product_image
import send_image
import products
import product
import config
import database
import profile_tab
import purchase
import ticket
import root
import os
from flask import url_for

@app.after_request
def set_no_cache(response):
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

@app.context_processor
def inject_version():
    return dict(html_version=app.config['HTML_VERSION'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8888, debug=True, allow_unsafe_werkzeug=True)