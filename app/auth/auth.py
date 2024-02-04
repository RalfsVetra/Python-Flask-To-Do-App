import sqlite3
import contextlib
import re
import os
import hashlib
import uuid

from flask import (
    render_template, session,
    request, redirect, Blueprint
)

from dotenv import load_dotenv
from app.utils import set_session
from app.database import s_database
from app.utils import logged_protected

auth_bp = Blueprint('auth', __name__)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

database = "database.db"
s_database(db_f=database)


@auth_bp.route('/login', methods=['GET', 'POST'])
@logged_protected
def login():
    if request.method == 'GET':
        token = uuid.uuid4()
        session['token'] = token

        return render_template('auth/login.html', token=token)

    email = request.form.get('email')
    password = request.form.get('password')
    token = request.form.get('token')

    if str(token) != str(session['token']):
        return render_template('auth/login.html', message='Notikusi kritiksa kļūda!', token=token)

    ip_address = request.remote_addr
    attempts_left = get_attempts_left(ip_address)

    if attempts_left <= 1:
        return render_template('auth/login.html', message='Pārāk daudz pieteikšanās mēģinājumu. Sazinities ar administratoru, lai novērstu kļūdu!', token=token)

    sql_query = 'SELECT password, email FROM accounts WHERE email = ?'
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            account = conn.execute(sql_query, (email,)).fetchone()

    if not account:
        update_login_attempts(ip_address, attempts_left - 1)

        return render_template('auth/login.html', message='Nepareizs e-pasts!', token=token)

    hashed_password = hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()
    if hashed_password != account[0]:
        update_login_attempts(ip_address, attempts_left - 1)

        return render_template('auth/login.html', message='Nepareiza parole!', token=token)

    clear_login_attempts(ip_address)

    set_session(
        email=account[1]
    )

    return redirect('/')


@auth_bp.route('/register', methods=['GET', 'POST'])
@logged_protected
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')

    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    email = request.form.get('email')

    if len(password) < 4:
        return render_template('auth/register.html', message='Jūsu parolei jābūt 4 vai vairāk rakstzīmēm!')

    if password != confirm_password:
        return render_template('auth/register.html', message='Paroles nesakrīt!')

    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return render_template('auth/register.html', message='Nederīgs e-pasta formāts!')

    if not 3 < len(email) < 26:
        return render_template('auth/register.html', message='Lietotājvārdam jābūt no 4 līdz 25 rakstzīmēm.')

    sql_query = 'SELECT email FROM accounts WHERE email = ?;'
    with contextlib.closing(sqlite3.connect(database)) as conn:
        result = conn.execute(sql_query, (email,)).fetchone()
    if result:
        return render_template('auth/register.html', message='E-pasts jau pastāv!')

    hash_password = hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()

    sql_query = 'INSERT INTO accounts(password, email) values (?, ?);'
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            conn.execute(sql_query, (hash_password, email))

    set_session(
        email=email
    )

    return redirect('/')


@auth_bp.route('/logout')
def logout():
    session.clear()
    session.permanent = False

    return redirect('/login')


def get_attempts_left(ip_address):
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.execute('SELECT attempts_left FROM login_attempts WHERE ip_address = ?', (ip_address,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 3


def update_login_attempts(ip_address, attempts_left):
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            cursor = conn.execute('SELECT COUNT(*) FROM login_attempts WHERE ip_address = ?', (ip_address,))
            count = cursor.fetchone()[0]

            if count > 0:
                conn.execute('UPDATE login_attempts SET attempts_left = ? WHERE ip_address = ?',
                             (attempts_left, ip_address))
            else:
                conn.execute('INSERT INTO login_attempts (ip_address, attempts_left) VALUES (?, ?)',
                             (ip_address, attempts_left))


def clear_login_attempts(ip_address):
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            conn.execute('DELETE FROM login_attempts WHERE ip_address = ?', (ip_address,))
