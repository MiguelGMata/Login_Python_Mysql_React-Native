from flask import Flask
from routes.routesUser import routes_user
from flask_cors import CORS


app = Flask(__name__)


CORS(app, resources={r"/todo/*": {"origins": "http://localhost:3000/" }})


app.register_blueprint(routes_user, url_prefix="/api")

@app.route('/')
def index():
    return "<h1>Serveur en route dans le port 3000.</h1>"
