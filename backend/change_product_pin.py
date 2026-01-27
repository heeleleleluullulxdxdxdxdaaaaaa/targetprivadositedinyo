
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User, Product

@app.route("/profile/change-product-pin/<int:product_id>", methods=["GET"])
def profile_change_product_pin(product_id):

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        flash("Product not found in database")
        return redirect("/profile/my_products")
        
    try:
        product.pin = not product.pin
        db.session.commit()
        flash("Pin status successfully updated")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
    
    return redirect("/profile/my_products")