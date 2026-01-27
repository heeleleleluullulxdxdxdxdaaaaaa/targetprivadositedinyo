from config import app, bot
from flask import request, flash, redirect, url_for, session, render_template
from database import db, User
from utils import validate_email

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if not username or not password or not email:
            flash('Username, password and email are required!')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        if len(username) < 4:
            flash('Minimal username lenght: 4')
            return redirect(url_for('register'))
        
        if len(username) > 20:
            flash('Maximal username lenght: 20')
            return redirect(url_for('register'))
        
        if len(password) < 8:
            flash('Minimal password lenght: 8')
            return redirect(url_for('register'))
        
        if len(password) > 100:
            flash('Maximal password lenght: 100')
            return redirect(url_for('register'))
        
        if not validate_email(email):
            flash('Incorrect email')
            return redirect(url_for('register'))            
        
        try:

            new_user = User(
                email=email,
                username=username,
                password=password
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            session['user_id'] = new_user.id
            flash('Registration successful!')
            bot.send_message(chat_id=app.config['TELEGRAM_CHAT_ID'],
                             text=(
                                 f"User: {username} (id: {new_user.id})\nRegistred"
                             ))
            return redirect(url_for('root'))
            
        except Exception as e:
            
            db.session.rollback()
            flash('An error occurred during registration')
            return redirect(url_for('register'))
    
    return render_template('register.html')