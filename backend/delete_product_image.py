from config import app
from flask import session, redirect, url_for, flash
from database import db, User, Product, Order

@app.route('/profile/delete-product-image/<int:product_id>/<int:image_num>', methods=["GET"])
def profile_delete_product_image(product_id, image_num):

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
    
    image_num = str(image_num)

    try:
        if image_num == "1":
            if str(product.image2) == "None" and str(product.image3) == "None":
                flash("One image requaried")
                return redirect(f"/profile/change-product/{product_id}")
            else:
                product.image1 = product.image2
                product.image2 = product.image3
                product.image3 = "None"
        elif image_num == "2":
            if str(product.image3) == "None":
                product.image2 = "None"
            else:
                product.image2 = product.image3
                product.image3 = "None"
        elif image_num == "3":
            product.image3 = "None"
        db.session.commit()
        flash("Image succesfully deleted")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')

    return redirect(f"/profile/change-product/{product_id}")