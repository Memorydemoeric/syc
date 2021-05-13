import hashlib
import uuid


def encrypt_password_by_md5(your_string):
    m1 = hashlib.md5()
    m1.update(your_string.encode('utf-8'))
    return m1.hexdigest()


def get_uuid():
    uid = str(uuid.uuid4())
    return uid