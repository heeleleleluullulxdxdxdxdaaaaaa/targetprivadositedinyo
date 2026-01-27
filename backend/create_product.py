
from config import app
from flask import request, session, redirect, url_for, flash
from database import db, User, Product
from utils import save_upload, save_source, convert_youtube_to_embed

@app.route("/profile/create-product", methods=["post"])
def profile_create_product():

    user_id = session.get("user_id")
    if not user_id:
        flash("Please login first")
        return redirect("/login")
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("User not found in database")
        return redirect("/login")
    
    if not (user.seller or user.admin):
        flash("No access")
        return redirect("/profile/general_information")
    
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

    video_link = convert_youtube_to_embed(request.form["video_link"])
    source = save_source(request.files.get("filename"))

    if not in_stock or not category or not name or not price or not description or not preview_image1 or not source:
        flash("Fields not found")
        return redirect("/profile/general_information")
    
    try:
        product = Product(
            seller_id=user_id,
            category=category,
            name=name,
            price=price,
            in_stock=in_stock,
            description=description,
            filename=source,
            link_to_video=video_link,
            image1=preview_image1,
            image2=preview_image2,
            image3=preview_image3,
            pin=False
        )
        db.session.add(product)
        db.session.commit()
        flash("Product successfully uploaded")
        return redirect(f"/product/{product.name}")
    except Exception as e:
        db.session.rollback()
        flash(f'Database error: {str(e)}')
        
    return redirect("/profile/general_information")