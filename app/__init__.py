from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import create_engine
import os


app = Flask(__name__)
api = Api(app)

app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine('postgresql+psycopg2://postgres:Hearty160@localhost/bucket_list')

from db import models
from app import views
