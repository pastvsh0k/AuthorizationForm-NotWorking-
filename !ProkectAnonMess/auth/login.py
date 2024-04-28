from flask import Blueprint, render_template, request, redirect, session
import pymysql.cursors

auth_bp = Blueprint('auth', __name__)

# Параметри підключення до бази даних
connection = pymysql.connect(
  host='127.0.0.1',
  user='rootv2',
  password='12345',
  database='Credentials',
  cursorclass=pymysql.cursors.DictCursor
)

# Авторизація
@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form["email"]
    password = request.form["password"]

    # Виконання запиту до бази даних для перевірки наявності користувача
    with connection.cursor() as cursor:
      sql = "SELECT * FROM Users WHERE Email = %s"
      cursor.execute(sql, (email,))
      user = cursor.fetchone()

    if user and user['Password'] == password:  # Перевірка відкритого тексту пароля
      session['user_id'] = user['id']
      return redirect("/")  # Перенаправлення на головну сторінку
    else:
      return "Incorrect Email or Password"
  else:
    return render_template("AuthForm.html")
