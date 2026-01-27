from flask import Flask

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Serve any other routes as the main page
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)