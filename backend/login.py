from config import app
from flask import request, session, redirect, url_for, render_template, flash
from database import User

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id

            if user.admin:
                session['admin_access'] = True

            flash(f"Welcome, dear user.")
            return redirect(url_for('root'))
        else:
            flash('Invalid username or password!', "error")
            return redirect(url_for('login'))
    
    return render_template('login.html')