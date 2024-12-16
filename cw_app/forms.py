from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sqlalchemy.exc import IntegrityError
#EqualTo нужен для того, чтобы сравнивать значения в полях и узнавать, точно ли они одинаковые

#Импортируем модель User из нашего модуля
from cw_app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', default='', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', default='', validators=[DataRequired(), Email()])
    password = PasswordField('Password', default='', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', default='', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    #Создаём функции для проверки уникальности имени пользователя и почты
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует.') #raise для генерации исключений похожее на try-except

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такая почта уже используется.')

#Создание класса LoginForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Запомни меня') #создание галочки с подписью
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    new_username = StringField('New Username', default='', validators=[Length(min=2, max=20)])
    new_email = StringField('New Email', default='', validators=[Email()])
    new_password = PasswordField('New Password', default='', validators=[Length(min=2, max=10)])
    confirm_new_password = PasswordField('Confirm New Password', default='', validators=[EqualTo('new_password')])
    submit_change = SubmitField('Change')

    # Создаём функции для проверки уникальности имени пользователя и почты
    def validate_username(self, new_username):
        user = User.query.filter_by(username=new_username.data).first()
        if user:
            raise IntegrityError('Такое имя уже существует.')  # raise для генерации исключений похожее на try-except

    def validate_email(self, new_email):
        user = User.query.filter_by(email=new_email.data).first()
        if user:
            raise IntegrityError('Такая почта уже используется.')