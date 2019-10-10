__version__ = '1.0.0.dev0'


def setup(app, *args, **kwargs):
    from .numpydoc import setup
    return setup(app, *args, **kwargs)
