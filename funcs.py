
from flask import request

from models import User


def check_auth():
    if "Authorization" not in request.headers:
        raise Exception("Invalid request")
