from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Создаём приложения и настраиваем базу данных:
app = Flask(__name__)
# Настраиваем базу данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# Эта строчка отключает сигнализацию об изменении объектов внутри базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Создание объекта, через который мы будем работать с базой данных

#Создаём модель User (таблицу в БД)
# В скобках указываем модель, чтобы в дальнейшем создать именно базу данных
# id — целое число, первичный ключ.
# username — строка длиной до 80 символов, уникальная, не может быть пустой.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # В скобках описываем поля таблицы

    # Метод определяет, как объект модели будет выглядеть в виде строки
    def __repr__(self):
        return f'<User {self.username}>'

#Создаём БД и  таблицу в базе данных
# Функция создаёт контекст приложения, который нужен для работы с базой данных
with app.app_context():
# Создание всей таблицы, которые определены в классе User
    db.create_all()

#Работа с базой данных
#Добавление новых пользователей
#Создаём маршрут для добавления пользователей
# Сессия — временное хранилище перед добавлением в базу данных
@app.route('/add_user') # С помощью декоратора создаём маршрут, который будет вызывать функцию
def add_user(): # Функция будет создавать объект класса User
    new_user = User(username='new_username')
    db.session.add(new_user) # Добавляем в сессию
    db.session.commit() #  Сохраняем изменения в базу данных
    return 'User added' # Вывод сообщения о том, что юзер добавлен в базу данных

#Получение данных из базы данных
#Создаём маршрут для получения всех пользователей
@app.route('/users')
def get_users():
    users = User.query.all() # Получаем всех юзеров из базы данных и сохраняем в переменную users
    return str(users)







