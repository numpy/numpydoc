# Configure test collection to skip doctests for modules that depend on sphinx
# when sphinx is not available in the environment.

try:
    import sphinx

    has_sphinx = True
except ImportError:
    has_sphinx = False


collect_ignore = []

if not has_sphinx:
    collect_ignore += ["numpydoc/numpydoc.py", "numpydoc/docscrape_sphinx.py"]
