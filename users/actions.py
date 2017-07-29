import string
import random
import hashlib
from . import models

def isLoggedIn(request):
    if 'userMail' in request.session:
        return True
    else:
        return False

def encrypt(password, salt):
    salted = salt[:1] + password[:len(password) // 2] + \
             salt[1:len(salt) // 2 + 1] + password[len(password) // 2:] + salt[len(salt) // 2 + 1:]
    hashed = hashlib.sha3_256(bytes(salted, encoding='utf-8'))
    return hashed.hexdigest()

def generateSalt(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
