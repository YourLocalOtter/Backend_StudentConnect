import bcrypt

def hash_pwd(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_pwd(potiential_passowrd, hashed):
    return bcrypt.checkpw(potiential_passowrd.encode('utf-8'), hashed)