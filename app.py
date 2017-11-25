from flask import *
from flask_socketio import *
from passlib.hash import pbkdf2_sha256
from database import Session as Ss
from models import User
import re


app = Flask(__name__)

app.config['SECRET_KEY'] = '4v2sVZKZ5x6ln1ht4WnF'


@app.route('/dashboard')
def dashboard():
    if 'user_name' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('signin'))


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    result = "0"
    if request.method == "POST":
        email = request.json['email']
        user_name = request.json['user_name']
        password = pbkdf2_sha256.hash(request.json['password'])
        mac_address = request.json['mac_address']

        if email and user_name and password and mac_address:
            mac_pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
            email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            mac_re_pattern = re.compile(mac_pattern)
            email_re_pattern = re.compile(email_pattern)

            if mac_re_pattern.match(mac_address) and email_re_pattern.match(email):
                query = Ss.query(User).filter_by(user_name=user_name, mac_address=mac_address)
                if query.count() > 0:
                    result = "1"
                else:
                    user = User(email_address=email,
                                user_name=user_name,
                                password=password,
                                mac_address=mac_address)
                    try:
                        Ss.add(user)
                        Ss.commit()
                        result = "2"
                    except:
                        Ss.rollback()
                        result = "1"

    return result


@app.route('/auth', methods=['POST'])
def auth():
    if request.method == "POST":
        user_name = request.form['user_name']
        password = request.form['password']

        if user_name and password:
            user = Ss.query(User).filter_by(user_name=user_name).first()

            if user is not None and pbkdf2_sha256.verify(password, user.password) is True:
                session['user_name'] = user_name
                session.pop('msg', None)
                return redirect(url_for('dashboard'))

    session['msg'] = "auth failed"
    return redirect(url_for('signin'))


if __name__ == "__main__":
    app.run(debug=True)
