import os
import json
import datetime
from flask import Flask
from flask_mongoengine import MongoEngine
from app.api.controllers import api_module

app = Flask(__name__)

app.config.update(
    MONGODB_HOST='localhost',
    MONGODB_PORT='27017',
    MONGODB_DB='office_drive',
)

db = MongoEngine(app)

app.register_blueprint(api_module)