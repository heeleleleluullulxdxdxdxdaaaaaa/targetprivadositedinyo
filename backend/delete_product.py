from config import app
from flask import session, redirect, url_for, flash
from database import db, User, Product, Order

@app.route('/profile/delete-product/<int:product_id>', methods=["GET"])
def profile_delete_product(product_id):

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
    
    if str(product.seller_id) != str(user_id):
        flash("Is not your product")
        return redirect("/profile/my_products")
    
    orders = Order.query.filter_by(product_id=product.id).all()
    try:
        for order in orders:
            db.session.delete(order)
        db.session.delete(product)
        db.session.commit()
        flash("Product succesfully deleted")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')

    return redirect("/profile/my_products")