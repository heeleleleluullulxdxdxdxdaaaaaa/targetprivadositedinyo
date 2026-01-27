
from config import app
from flask import session, redirect, url_for, flash

@app.route('/logout')
def logout():

    session.pop('user_id', None)
    session.pop('admin', None)
    flash("⭐ Glad to see you")
    return redirect(url_for('root'))