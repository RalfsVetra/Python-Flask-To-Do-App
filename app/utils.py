from flask import redirect, url_for, session
from functools import wraps


def login_protected(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('auth.login'))

        return func(*args, **kwargs)

    return decorator


def logged_protected(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'email' in session:
            return redirect(url_for('home.home'))

        return func(*args, **kwargs)

    return decorator


def set_session(email: str) -> None:
    session['email'] = email
