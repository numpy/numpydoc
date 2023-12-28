"""Test module for hook."""  # numpydoc ignore=ES01,SA01


def some_function(name):
    """Welcome to some function."""
    pass


class MyClass:
    """This is MyClass."""

    def __init__(self):
        pass

    def __repr__(self):  # numpydoc ignore=GL08
        pass

    def do_something(self, *args, **kwargs):
        """
        Do something.

        Parameters
        ----------
        *args
        """
        pass

    def process(self):
        """Process stuff."""
        pass


class NewClass:
    pass
