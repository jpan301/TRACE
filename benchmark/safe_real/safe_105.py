# source: DjangoSafe / django/contrib/auth/hashers.py
# function: encode

class MD5PasswordHasher:
    def encode(self, password, salt):
        self._check_encode_args(password, salt)
        password = force_str(password)
        salt = force_str(salt)
        hash = hashlib.md5((salt + password).encode()).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)