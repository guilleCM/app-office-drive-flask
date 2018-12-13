from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from config import ProductionConfig

app = Flask(__name__)
app.config.from_object(ProductionConfig)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


db = MongoEngine(app)
jwt = JWTManager(app)

from app.api.controllers import api_module
app.register_blueprint(api_module)
