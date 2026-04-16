# source: DjangoSafe / django/contrib/auth/hashers.py
# function: encode

class PBKDF2PasswordHasher:
    def encode(self, password, salt, iterations=None):
        self._check_encode_args(password, salt)
        iterations = iterations or self.iterations
        password = force_str(password)
        salt = force_str(salt)
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode("ascii").strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)