from flask import *
from flask import make_response
from passlib.hash import pbkdf2_sha256
from database import Session as Ss
from models import User
import re
import os
from base64 import b64encode
from werkzeug.utils import secure_filename


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif', 'svg', 'tif', 'tiff', 'bmp', 'ico'])

app.config['SECRET_KEY'] = '4v2sVZKZ5x6ln1ht4WnF'
app.config['UPLOAD_FOLDER'] = "./client_images"


@app.route('/dashboard')
def dashboard():
    if 'user_name' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('signin'))


@app.route('/usage')
def usage():
    if 'user_name' in session:
        return render_template('usage.html')
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


@app.route('/client_images/<image_path>', methods=['GET'])
def get_image(image_path):
    avatar = app.config['UPLOAD_FOLDER'] + "/" + image_path
    f = open(avatar, 'rb+')
    data = f.read()
    resp = make_response(data)
    resp.content_type = "image/jpeg"
    f.close()
    return resp


@app.route('/setting')
def setting():
    if 'user_name' in session:
        user = Ss.query(User).filter_by(user_name=session['user_name']).one()
        if user.avatar is not None:
            f = open(user.avatar, 'rb+')
            data = f.read()
            profile_image = b64encode(data)
            f.close()
            Ss.close()
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
            Ss.close()

            if user is not None and pbkdf2_sha256.verify(password, user.password) is True:
                session['user_name'] = user_name
                session.pop('msg', None)
                return redirect(url_for('dashboard'))

    session['msg'] = "auth failed"
    return redirect(url_for('signin'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/edit_profile', methods=['POST'])
def change_profile_image():
    if request.method == "POST":
        if request.files['avatar']:
            avatar = request.files['avatar']
            if avatar and allowed_file(avatar.filename):
                file_extension = avatar.filename.rsplit('.', 1)[1].lower()
                avatar.filename = str(session['user_name']) + '.' + str(file_extension)
                filename = secure_filename(avatar.filename)
                avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user = Ss.query(User).filter_by(user_name=session['user_name']).one()
                user.avatar = str(app.config['UPLOAD_FOLDER'] + "/" + filename)
                Ss.commit()
                Ss.close()

        if request.form['username']:
            user = Ss.query(User).filter_by(user_name=session['user_name']).one()
            user.user_name = request.form['username']
            session['user_name'] = request.form['username']
            Ss.commit()
            Ss.close()

    return redirect('setting')


@app.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        match_user = Ss.query(User).filter_by(user_name=user_name).one()
        Ss.delete(match_user)
        Ss.commit()
        Ss.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
