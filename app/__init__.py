from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config.update(
    MONGODB_HOST='localhost',
    MONGODB_PORT=27017,
    MONGODB_DB='office_drive',
)
db = MongoEngine(app)

app.config['JWT_SECRET_KEY'] = "jwt-secret-string"
jwt = JWTManager(app)

from app.api.controllers import api_module
app.register_blueprint(api_module)
