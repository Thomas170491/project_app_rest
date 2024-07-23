from functools import wraps
from flask import request,jsonify
from .jwt_utils import decode_jwt

def jwt_required_with_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'error': 'Bearer token malformed'}), 401
            else:
                return jsonify({'error': 'Authorization header is missing'}), 401

            payload, error = decode_jwt(token)
            if error:
                return jsonify({'error': error}), 401

            if payload['role'] != role:
                return jsonify({'error': 'Unauthorized role'}), 403

            request.user = payload  # Attach user info to request for later use
            return fn(*args, **kwargs)
        return decorator
    return wrapper
