from flask import *

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')
