import base64
import hashlib
import hmac

from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def get_one(self, uid):
        return self.dao.get_by_user_id(uid)

    def get_all(self):
        users = self.dao.get_all()
        return users

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.get_hash(user_d["password"])
        self.dao.update(user_d)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)

        return  base64.b64encode(hash_digest)

    def compare_password(self, password, other_password):
        decoded_hash = base64.b64decode(password)
        hash_other_password = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)
        return hmac.compare_digest(decoded_hash, hash_other_password)