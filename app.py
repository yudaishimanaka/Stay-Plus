from flask import *
from webui import web
from flask_socketio import *
from database import Session as Ss
from models import User
import re


app = Flask(__name__)
app.register_blueprint(web.app)


@app.route('/register', methods=['POST'])
def register():
    result = "0"
    if request.method == "POST":
        email = request.json['email']
        user_name = request.json['user_name']
        password = request.json['password']
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
                    Ss.add(user)
                    Ss.commit()
                    result = "2"

    return result


if __name__ == "__main__":
    app.run(debug=True)
