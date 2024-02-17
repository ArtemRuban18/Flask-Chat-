from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO


app  = Flask(__name__, template_folder=r'C:\Users\User\OneDrive\Рабочий стол\Flask Chat\app\templates',
             static_folder=r'C:\Users\User\OneDrive\Рабочий стол\Flask Chat\app\static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key= 'it`s super secret key!'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

from app import routes, models, forms, events