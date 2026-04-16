# source: DjangoSafe / django/utils/termcolors.py
# function: make_style

def make_style(opts=(), **kwargs):
    """
    Return a function with default parameters for colorize()

    Example:
        bold_red = make_style(opts=('bold',), fg='red')
        print(bold_red('hello'))
        KEYWORD = make_style(fg='yellow')
        COMMENT = make_style(fg='blue', opts=('bold',))
    """
    return lambda text: colorize(text, opts, **kwargs)