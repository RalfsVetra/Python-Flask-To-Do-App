import contextlib
import sqlite3

from flask import Blueprint, render_template, request, redirect, session
from app.utils import login_protected

home_bp = Blueprint('home', __name__)

database = "database.db"


@home_bp.route('/', methods=['GET', 'POST'])
@login_protected
def home():
    email = session.get('email')

    if request.method == 'GET':
        sql_query = 'SELECT id, note FROM notes WHERE user_id = (SELECT id FROM accounts WHERE email = ?)'
        with contextlib.closing(sqlite3.connect(database)) as conn:
            with conn:
                notes_data = conn.execute(sql_query, (email,)).fetchall()

        return render_template('home/home.html', notes_data=notes_data)

    if request.method == 'POST':
        note = request.form.get('note')

        sql_query = 'SELECT id FROM accounts WHERE email = ?'
        with contextlib.closing(sqlite3.connect(database)) as conn:
            with conn:
                user_id = conn.execute(sql_query, (email,)).fetchone()[0]

        sql_query = 'INSERT INTO notes (user_id, note) VALUES (?, ?)'
        with contextlib.closing(sqlite3.connect(database)) as conn:
            with conn:
                conn.execute(sql_query, (user_id, note))

        return redirect('/')


@home_bp.route('/delete-note', methods=['GET','POST'])
@login_protected
def delete_note():
    if request.method != 'POST':
        return redirect('/')

    note_id = request.form.get('note_id')
    email = session.get('email')

    sql_query = 'DELETE FROM notes WHERE id = ? AND user_id = (SELECT id FROM accounts WHERE email = ?)'
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            conn.execute(sql_query, (note_id, email))

    return redirect('/')
