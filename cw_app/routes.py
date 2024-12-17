from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from cw_app import app, db
from cw_app.models import User
from cw_app.forms import RegistrationForm, LoginForm, AccountForm
import bcrypt #помогает зашифровать пароли, чтобы не хванить их в обчном виде
from werkzeug.security import generate_password_hash, check_password_hash
#`generate_password_hash` не существует в модуле `bcrypt`.
# Эта функция обычно ассоциируется с библиотекой `werkzeug.security`, а не `bcrypt`
from sqlalchemy.exc import IntegrityError


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

    # form.validate_on_submit проверяет, была ли форма отправлена с помощью метода HTTP POST и прошла ли она валидацию.
    # Это удобно, потому что позволяет обработать форму только в том случае,
    # если она была отправлена и все поля формы корректны
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
    #`current_user` — это объект, который предоставляет информацию о текущем пользователе, взаимодействующем с приложением
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
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    user = User.query.filter_by(email=current_user.email).first()
    print(user)
    if request.method == 'POST':
        if form.new_username.data != '' and form.new_username.validate(form):
            try:
                user.username = form.new_username.data
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Такое имя уже существует! Попробуйте ввести другое имя.','danger')
        if form.new_email.data != '' and form.new_email.validate(form):
            try:
                user.email = form.new_email.data
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Такая почта уже используется!','danger')
        if form.new_password.data != '' and form.new_password.validate(form):
            user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        if form.new_email.data != '' or form.new_password.data != '':
            flash('Вы успешно изменили данные! Войдите заново', 'success')
            return redirect(url_for('logout'))

    return render_template('account.html', form=form)