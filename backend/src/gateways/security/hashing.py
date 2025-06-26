import bcrypt


class BcryptHasher:
    def hash(self, s: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(s.encode(), salt)

    def compare(self, s: str, hash: bytes) -> bool:
        return bcrypt.checkpw(s.encode(), hash)
