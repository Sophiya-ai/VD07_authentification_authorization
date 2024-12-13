from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRETE_KEY'] = 'your_secrete_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#Создаём объект Bcrypt
bcrypt = Bcrypt(app)

#Создаём объект LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Модуль будет перенаправлять пользователя на маршрут, который мы указываем (на авторизацию)

from cw_app import routes


