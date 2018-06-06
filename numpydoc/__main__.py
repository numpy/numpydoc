import argparse
import importlib
import ast

from .docscrape_sphinx import get_doc_object


def main(argv=None):
    """Test numpydoc docstring generation for a given object"""

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('import_path', help='e.g. numpy.ndarray')

    def _parse_config(s):
        key, _, value = s.partition('=')
        value = ast.literal_eval(value)
        return key, value

    ap.add_argument('-c', '--config', type=_parse_config,
                    action='append',
                    help='key=val where val will be parsed by literal_eval, '
                         'e.g. -c use_plots=True. Multiple -c can be used.')
    args = ap.parse_args(argv)

    parts = args.import_path.split('.')

    for split_point in range(len(parts), 0, -1):
        try:
            path = '.'.join(parts[:split_point])
            obj = importlib.import_module(path)
        except ImportError:
            continue
        break
    else:
        raise ImportError('Could not resolve {!r} to an importable object'
                          ''.format(args.import_path))

    for part in parts[split_point:]:
        obj = getattr(obj, part)

    print(get_doc_object(obj, config=dict(args.config or [])))

if __name__ == '__main__':
    main()
