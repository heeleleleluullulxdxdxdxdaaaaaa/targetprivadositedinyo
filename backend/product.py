from config import app
from flask import session, redirect, url_for, render_template, flash
from database import User, Order, Product

@app.route('/product/<string:product_name>', methods=['GET'])
def product(product_name):
        
    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    product = Product.query.filter_by(name=product_name).first()
    if not product:
        flash("Product not found in database")
        return redirect("/")
    
    seller = User.query.filter_by(id=product.seller_id).first()
    if not seller:
        flash("Seller not found in database")
        return redirect("/")
    
    if not (seller.admin or seller.seller):
        flash("This user dont have permises")
        return redirect("/")
    
    return render_template(f'product.html', 
                            user_id=user_id,
                            seller_id=seller.id,
                            product_id=product.id)