import hmac
import hashlib
import base64
import json 
import datetime
from config import secret_key

def create_jwt(payload): 
    payload = json.dumps(payload).encode()
    header = json.dumps({
        'typ': 'JWT',
        'alg': 'HS256'
    }).encode()
    b64_header = base64.urlsafe_b64encode(header).decode()
    b64_payload = base64.urlsafe_b64encode(payload).decode()
    signature = hmac.new(
        key=secret_key.encode(),
        msg=f'{b64_header}.{b64_payload}'.encode(),
        digestmod=hashlib.sha256
    ).digest()
    jwt = f'{b64_header}.{b64_payload}.{base64.urlsafe_b64encode(signature).decode()}'
    return jwt

def verify_and_decode_jwt(jwt):
    b64_header, b64_payload, b64_signature = jwt.split('.')
    b64_signature_checker = base64.urlsafe_b64encode(
        hmac.new(
            key=secret_key.encode(),
            msg=f'{b64_header}.{b64_payload}'.encode(),
            digestmod=hashlib.sha256
        ).digest()
    ).decode()

    # payload extraido antes para checar o campo 'exp'
    payload = json.loads(base64.urlsafe_b64decode(b64_payload))
    unix_time_now = datetime.datetime.now().timestamp()

    if payload.get('exp') and payload['exp'] < unix_time_now:
        return 'Token expirado', 401
    
    if b64_signature_checker != b64_signature:
        return 'Assinatura inválida', 401
    
    return 'OK'    

def iniciandoJWT(userId, Role): # USA O create_jwt.
    payload = {
        # id
        # Role
        'userId': userId,
        'role' : Role,
        'exp': (datetime.datetime.now() + datetime.timedelta(minutes=60)).timestamp(),
    }
    jwt_created = create_jwt(payload)
    return jwt_created