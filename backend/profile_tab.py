from config import app
from flask import session, redirect, url_for, render_template, flash
from database import User, Order, Product, Ticket

@app.route('/profile/<string:tab_name>', methods=['GET'])
def profile_tab(tab_name):
        
    user_id = session.get('user_id')

    if not user_id:
        flash('Please login first!')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User not found!')
        return redirect(url_for('login'))
    
    if tab_name == "general_information":

        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id)
    
    elif tab_name == "purchases":  

        product_ids = []
        orders = Order.query.filter_by(user_id=user_id).all()
        for order in orders:
            product_ids.append(order.product_id)

        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id,
                                product_ids=product_ids)
    
    elif tab_name == "active_tickets":

        view = "User"
        if not (user.seller or user.admin):
            tickets = Ticket.query.filter_by(user_id=user_id).all()
        else:
            view = "Seller"
            if user.admin:
                tickets = Ticket.query.all()
            else:
                tickets = Ticket.query.filter_by(seller_id=user_id).all()
        
        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id,
                                tickets=tickets,
                                view=view)
    
    elif tab_name == "payment_details":

        if not (user.seller or user.admin):
            flash("No access")
            return redirect("/profile/general_information")
        
        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id)
    
    elif tab_name == "information":

        if not (user.seller or user.admin):
            flash("No access")
            return redirect("/profile/general_information")
        
        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id)
    
    elif tab_name == "my_products":

        if not (user.seller or user.admin):
            flash("No access")
            return redirect("/profile/general_information")
        
        products = Product.query.filter_by(seller_id=user_id).all()

        product_ids = []
        for product in products:
            product_ids.append(product.id)
        
        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id,
                                product_ids=product_ids)
    
    elif tab_name == "create_product":

        if not (user.seller or user.admin):
            flash("No access")
            return redirect("/profile/general_information")
        
        return render_template(f'profile/{tab_name}.html', 
                                user_id=user_id)