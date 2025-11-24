"""Test module for hook."""  # numpydoc ignore=ES01,SA01


def some_function(name):
    """Welcome to some function."""


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

    def create(self):
        """Creates stuff."""


class NewClass:
    class GoodConstructor:
        """
        A nested class to test constructors via AST hook.

        Implements constructor via class docstring.

        Parameters
        ----------
        name : str
            The name of the new class.
        """

        def __init__(self, name):
            self.name = name

    class BadConstructor:
        """
        A nested class to test constructors via AST hook.

        Implements a bad constructor docstring despite having a good class docstring.

        Parameters
        ----------
        name : str
            The name of the new class.
        """

        def __init__(self, name):
            """
            A failing constructor implementation without parameters.
            """
            self.name = name
