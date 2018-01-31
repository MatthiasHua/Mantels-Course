from random import choice
import hashlib
import string

def create_key(length=16,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def verificate(number, token):
    return hashlib.sha1((number + token).encode("utf8")).hexdigest()
