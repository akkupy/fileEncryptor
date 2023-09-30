from cryptography.fernet import Fernet
import base64,hashlib


def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))


def encrypt(passcode,json):

    key = gen_fernet_key(passcode.encode('utf-8'))
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json)

    return encrypted

def decrypt(passcode,json):

    key = gen_fernet_key(passcode.encode('utf-8'))
    fernet = Fernet(key)
    decrypted = fernet.decrypt(json)

    return decrypted

