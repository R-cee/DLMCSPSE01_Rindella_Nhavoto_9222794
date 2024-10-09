from flask import abort
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

def admin_required(f):
    """
    Decorator to check if the current user has the 'Admin' role.
    If the user does not have the 'Admin' role, it will return a 403 Forbidden response.
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'].lower() != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

