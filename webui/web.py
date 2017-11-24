from flask import *

app = Blueprint('web', __name__)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')
