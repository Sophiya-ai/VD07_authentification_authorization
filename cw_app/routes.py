from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from cw_app import app, db
from cw_app.models import User
from cw_app.forms import RegistrationForm, LoginForm
import bcrypt #помогает зашифровать пароли, чтобы не хванить их в обчном виде
from werkzeug.security import generate_password_hash, check_password_hash
#`generate_password_hash` не существует в модуле `bcrypt`.
# Эта функция обычно ассоциируется с библиотекой `werkzeug.security`, а не `bcrypt`


#Создаём маршрут для главной страницы
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#Создаём маршрут для страницы регистрации, обрабатываем методы GET и POST
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#Создаём маршрут для страницы входа, также обрабатываем методы GET и POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные', 'danger')

    return render_template('login.html', form=form)

#Создаём маршрут для выхода из аккаунта.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#Создаём маршрут для отображения страницы аккаунта.
# Декоратор login_required требует, чтобы пользователь был авторизирован
@app.route('/account')
@login_required
def account():
    return render_template('account.html')