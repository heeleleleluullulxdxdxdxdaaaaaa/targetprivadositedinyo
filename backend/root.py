
from config import app
from flask import render_template

@app.route('/')
def root():
    return render_template('index.html')
    
@app.route('/index')
def old_index():
    return root()