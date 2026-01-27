from config import app
from flask import session, redirect, url_for, render_template, flash
from database import User, Order, Product

@app.route('/products/<string:seller_name>', methods=['GET'])
def products(seller_name):
        
    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    seller = User.query.filter_by(username=seller_name).first()
    if not seller:
        flash("Seller not found in database")
        return redirect("/")
    
    if not (seller.admin or seller.seller):
        flash("This user dont have permises")
        return redirect("/")

    pinned_products = Product.query.filter_by(seller_id=seller.id, pin=True).all()
    other_products = Product.query.filter_by(seller_id=seller.id, pin=False).all()

    all_products = []
    all_products = pinned_products + other_products

    product_ids = []
    for product in all_products:
        product_ids.append(product.id)
    
    return render_template(f'products.html', 
                            user_id=user_id,
                            seller_id=seller.id,
                            product_ids=product_ids)