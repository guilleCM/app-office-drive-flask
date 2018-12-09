from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from config import ProductionConfig

app = Flask(__name__)
app.config.from_object(ProductionConfig)

db = MongoEngine(app)
jwt = JWTManager(app)

from app.api.controllers import api_module
app.register_blueprint(api_module)
