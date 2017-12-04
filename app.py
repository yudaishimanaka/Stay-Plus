from flask import *
from passlib.hash import pbkdf2_sha256
from database import Session as Ss
from models import User
import re
import os
from base64 import b64encode


app = Flask(__name__)
UPLOAD_FOLDER = "/tmp"

app.config['SECRET_KEY'] = '4v2sVZKZ5x6ln1ht4WnF'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/signout')
def signout():
    session.pop('user_name', None)
    return redirect(url_for('signin'))


@app.route('/setting')
def setting():
    if 'user_name' in session:
        user = Ss.query(User).filter_by(user_name=session['user_name']).one()
        if user.avatar is not None:
            f = open(user.avatar, 'rb+')
            data = f.read()
            profile_image = b64encode(data)
            f.close()
            return render_template('setting.html', user=user, profile_image=profile_image.decode('utf-8'))
        else:
            return render_template('setting.html', user=user)
    else:
        return redirect(url_for('signin'))


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
                        Ss.close()
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


@app.route('/change_profile_image', methods=['POST'])
def change_profile_image():
    if request.method == "POST":
        avatar = request.files['avatar']
        filename = avatar.filename
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = Ss.query(User).filter_by(user_name=session['user_name']).one()
        user.avatar = str(app.config['UPLOAD_FOLDER'] + "/" + filename)
        Ss.commit()
        Ss.close()
        return redirect('setting')


if __name__ == "__main__":
    app.run(debug=True)
