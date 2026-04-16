# source: DjangoSafe / django/template/base.py
# function: __repr__

class Lexer:
    def __repr__(self):
        return '<%s template_string="%s...", verbatim=%s>' % (
            self.__class__.__qualname__,
            self.template_string[:20].replace("\n", ""),
            self.verbatim,
        )