from flask import *
from webui import web
from flask_socketio import *

app = Flask(__name__)
app.register_blueprint(web.app)



if __name__ == "__main__":
    app.run(debug=True)
