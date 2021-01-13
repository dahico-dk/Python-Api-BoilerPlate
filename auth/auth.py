from functools import wraps
from jwcrypto import jwt, jwk
import uuid
from flask import session, abort, request
import json


# adds given key to the session
def set_key(key, uid):
    session['auth_key'] = key
    # second layer of request track
    session['uid'] = uid


# creates a encrypted jwt token which contains session uuid as claim
def create_enc_token():
    key = jwk.JWK(generate='oct', size=256)
    uid = str(uuid.uuid4())
    set_key(key.export(), uid)
    token = jwt.JWT(header={"alg": "HS256"},
                    claims={"uid": uid})
    token.make_signed_token(key)
    etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                     claims=token.serialize())
    etoken.make_encrypted_token(key)
    return etoken.serialize()


# gets the key from session
def get_key():
    key = session.get('auth_key', 'not set')
    uid = session.get('uid', 'not set')
    return key, uid


# returns true or false. Compares uid with the payload
def decrypt(e):
    key, uid = get_key()
    ikey = jwk.JWK(**json.loads(key))
    et = jwt.JWT(key=ikey, jwt=e)
    st = jwt.JWT(key=ikey, jwt=et.claims)
    stdict = json.loads(st.claims)
    return stdict.get("uid")


# authentication decorator. Throws 401 on unvalid tokens
def requires_auth(permission=''):
    def requires_auth_deco(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = decrypt(token)
                # We can also use role based permissions too. We need a permission array and pass permission string as a parameter.
                # check_permissions(permission, payload)
                key, uid = get_key()
                if payload == uid:
                    return f()
                else:
                    abort(401)

            except Exception as e:
                abort(401)

        return wrapper

    return requires_auth_deco


def get_token_auth_header():
    """Gets token from the authorization header

    Returns:
       token: the token at authorization header as string

    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    """Checks permissions on payload
    Args:
        permission:required permission
        payload:decoded jwt
    Returns:
        Boolean
    """
    if 'permissions' not in payload:
        abort(401)

    if permission not in payload['permissions']:
        abort(401)

    return True


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
