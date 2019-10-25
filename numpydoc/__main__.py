import sys
import argparse
import importlib
import ast

from .docscrape_sphinx import get_doc_object
from .validate import validate


def render_object(import_path, config):
    """Test numpydoc docstring generation for a given object"""
    parts = import_path.split('.')

    for split_point in range(len(parts), 0, -1):
        try:
            path = '.'.join(parts[:split_point])
            obj = importlib.import_module(path)
        except ImportError:
            continue
        break
    else:
        raise ImportError('Could not resolve {!r} to an importable object'
                          ''.format(import_path))

    for part in parts[split_point:]:
        obj = getattr(obj, part)

    print(get_doc_object(obj, config=dict(config or [])))

    return 0


def validate_object(import_path):
    exit_status = 0
    results = validate(import_path)
    for err_code, err_desc in results["errors"]:
        exit_status += 1
        print(':'.join([import_path, err_code, err_desc]))
    return exit_status


if __name__ == '__main__':
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
    ap.add_argument('--validate', action='store_true',
                    help='validate the object and report errors')
    args = ap.parse_args()

    if args.validate:
        exit_code = validate_object(args.import_path)
    else:
        exit_code = render_object(args.import_path, args.config)

    sys.exit(exit_code)
