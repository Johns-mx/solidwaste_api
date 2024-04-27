import hashlib, base64, bcrypt, secrets, uuid
from datetime import datetime
from cryptography.fernet import Fernet
from app.index import SECRET_TOKEN_HASH


#>> Generate key and fernet
key_fernet = Fernet.generate_key()
fernet = Fernet(key_fernet)


def generate_uuid():
    return str(uuid.uuid4())


async def generate_token_keyuser():
    payload= datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    key= secrets.token_hex(20) + payload
    token= fernet.encrypt(key.encode("utf-8"))
    return token


class HashingManager(object):
    async def hash_password(self, password: str):
        #>> FUNCION PARA ENCRIPTAR EL PASSWORD DE USUARIO
        secret_key = bytes(SECRET_TOKEN_HASH, encoding='ascii')
        
        key = bcrypt.kdf(
            password=password.encode(),
            salt=secret_key,
            desired_key_bytes=64,
            rounds=100
        )
        passwd= base64.b64encode(hashlib.sha256(key).digest())
        return passwd
