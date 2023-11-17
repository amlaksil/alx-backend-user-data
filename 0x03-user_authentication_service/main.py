#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test register_user.
    """
    url = 'http://localhost:5000/users'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, data=data)
    expected_data = {'email': email, 'message': 'user created'}

    assert expected_data == response.json()

    response = requests.post(url, data=data)
    assert {'message': 'email already registered'} == response.json()


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Validate login password
    """
    url = 'http://localhost:5000/sessions'
    data = {
        'email': email,
        'password': password
        }
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Check
    """
    url = 'http://localhost:5000/sessions'
    data = {
        'email': email,
        'password': password
        }
    response = requests.post(url, data=data)
    session_id = response.cookies.get('session_id')
    assert response.json() == {'email': email, 'message': 'logged in'}
    return session_id


def profile_logged(session_id) -> None:
    """
    Check
    """
    url = 'http://localhost:5000/profile'
    data = {'session_id': session_id}
    response = requests.get(url, cookies=data)
    assert response.json() == {'email': 'guillaume@holberton.io'}


def log_out(session_id: str) -> None:
    """
    Check
    """
    url = 'http://localhost:5000/sessions'
    data = {'session_id': session_id}

    response = requests.delete(url, cookies=data)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Check
    """
    url = 'http://localhost:5000/reset_password'
    response = requests.post(url, data={'email': email})

    assert response.status_code == 200
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    """
    url = 'http://localhost:5000/reset_password'
    response = requests.put(url)

    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
