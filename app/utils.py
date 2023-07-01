from os import path

from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def build_file_path(file_path):
    return path.join(path.dirname(path.abspath(__file__)), file_path)
