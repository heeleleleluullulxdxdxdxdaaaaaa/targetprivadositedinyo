
from config import app, bot, NOWPAYMENTS_BASE_URL
from flask import session, url_for, redirect, flash, request, jsonify
from database import User, Product, Order, db
import requests
import json
import logging

@app.route('/purchase/<int:id>')
def purchase(id):

    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first!')
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User not found in database!')
        return redirect("/login")
    
    product = Product.query.filter_by(id=id).first()
    if not product:
        flash('Product not found in database!')
        return redirect("/")
    
    if product.in_stock > -1:
        if product.in_stock == 0:
            flash("This product cannot be purchased")
            return redirect("/")
    
    seller = User.query.filter_by(id=product.seller_id).first()
    if not seller or not seller.nowpayments_api_key:
        flash('Seller not found or not properly configured!')
        return redirect("/")
    
    if not (seller.admin or seller.seller):
        flash("This user have no permisions")
        return redirect("/")

    url = NOWPAYMENTS_BASE_URL + "/invoice"

    payload = json.dumps({
        "price_amount": float(product.price),  
        "price_currency": "usd",
        "order_id": f"user_{user.id}_product_{product.id}_seller_{seller.id}",
        "order_description": str(product.id),
        "ipn_callback_url": "https://ethereal-market.com/callback",
        "success_url": "https://ethereal-market.com/profile",
        "cancel_url": "https://ethereal-market.com/profile",
        "is_fixed_rate": True,
        "is_fee_paid_by_user": False
    })
    
    headers = {
        "x-api-key": str(seller.nowpayments_api_key),
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        invoice_url = response_data['invoice_url']
        return redirect(invoice_url)
    except requests.exceptions.RequestException as e:
        logging.error(f"NowPayments API error for seller {seller.id}: {e}")
        flash('Payment service temporarily unavailable')
        return redirect(url_for('root'))
    
@app.route('/callback', methods=["POST"])
def payment_callback():

    try:       
        
        received_signature = request.headers.get('x-nowpayments-sig')
        
        if not received_signature:
            logging.warning("No signature in callback headers")
            try:
                bot.send_message(chat_id=app.config['TELEGRAM_CHAT_ID'], text='❌ No signature in callback')
            except:
                pass
            return jsonify({"status": "error", "message": "Missing signature"}), 401
        
        if request.is_json:

            data = request.get_json()
            logging.info(f"Callback data: {data}")
            
            seller_id = None
            order_id = data.get('order_id', '')
            
            try:
                parts = order_id.split('_')
                seller_id = int(parts[5]) if len(parts) > 5 else None
            except (IndexError, ValueError):
                seller_id = None

            seller = None
            if seller_id:
                seller = User.query.filter_by(id=seller_id).first()
            
            if not seller and data.get('order_description'):
                try:
                    product_id = int(data.get('order_description'))
                    product = Product.query.filter_by(id=product_id).first()
                    if product:
                        if product.in_stock > -1:
                            product.in_stock -= 1
                        seller = User.query.filter_by(id=product.seller_id).first()
                except (ValueError, TypeError):
                    pass
            
            if data.get('payment_status') == "finished":

                product_id = data.get('order_description')
                order_id = data.get('order_id')
                
                try:
                    parts = order_id.split('_')
                    user_id = int(parts[1]) if len(parts) > 1 else None
                    seller_id = int(parts[5]) if len(parts) > 5 else None
                    
                    if product_id:
                        product_id = int(product_id)
                    
                except (IndexError, ValueError, TypeError) as e:
                    logging.error(f"Error parsing order_id {order_id}: {e}")
                    user_id = None
                    seller_id = None
                
                if product_id and user_id:
                    product = Product.query.filter_by(id=product_id).first()
                    if product:
                        order = Order(
                            user_id=user_id,
                            product_id=product_id,
                            seller_id=product.seller_id
                        )
                        db.session.add(order)
                        db.session.commit()
                        logging.info(f"Order created: user_id={user_id}, product_id={product_id}")
                        
                        try:
                            bot.send_message(
                                chat_id=app.config['TELEGRAM_CHAT_ID'], 
                                text=f'✅ Payment verified and successful!\nSeller: { User.query.filter_by(id=seller_id).first().username } (id: { seller_id })\nBuyer: { User.query.filter_by(id=user_id).first().username } (id: { user_id })\nProduct: { Product.query.filter_by(id=product_id).first().name } (${ Product.query.filter_by(id=product_id).first().price } (id: { product_id }))'
                            )   
                        except Exception as bot_error:
                            logging.error(f"Telegram bot error: {bot_error}")
            
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logging.error(f"Callback processing error: {e}")
        try:
            bot.send_message(chat_id=app.config['TELEGRAM_CHAT_ID'], text=f'❌ Callback error: {str(e)}')
        except:
            pass
        return jsonify({"status": "error", "message": str(e)}), 500
