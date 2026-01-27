
from config import app
from flask import request, session, redirect, flash, render_template
from database import db, User, Product
from utils import save_upload, save_source

@app.route("/profile/change-product/<int:product_id>", methods=["post", "get"])
def profile_change_product(product_id):

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    if request.method == "GET":
        return render_template(f'profile/change_product.html', 
                        user_id=user_id,
                        product_id=product_id)
    else:
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            flash("Product not found in database")
            return redirect("/profile/my_products")

        category = request.form["category"]
        name = request.form["name"]
        price = request.form["price"]
        in_stock = request.form["in_stock"]
        description = request.form["description"]
        preview_image1 = save_upload(request.files.get("preview_image1"))
        preview_image2 = save_upload(request.files.get("preview_image2"))
        preview_image3 = save_upload(request.files.get("preview_image3"))

        if preview_image2 == "None" and preview_image3 != "None":
            preview_image2 = preview_image3
            preview_image3 = "None"

        video_link = request.form["video_link"]
        source = save_source(request.files.get("filename"))

        try:
            product.category = category
            product.name = name
            product.price = price
            product.in_stock = in_stock
            product.description = description
            if preview_image1 != "None":
                product.image1 = preview_image1
            if preview_image2 != "None":
                product.image2 = preview_image2
            if preview_image3 != "None":
                product.image3 = preview_image3
            product.link_to_video = video_link
            if source != "None":
                product.filename = source

            db.session.commit()
            flash("Information successfully updated")
        except Exception as e:
            db.session.rollback()
            flash(f'Database error: {str(e)}')
    
    return redirect("/profile/my_products")