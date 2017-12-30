import re
from sphinx import addnodes


QUALIFIED_NAME_RE = re.compile(
    # e.g int, numpy.array, ~numpy.array
    r'^'
    r'[~\.]?'
    r'[a-zA-Z_]\w*'
    r'(?:\.[a-zA-Z_]\w*)*'
    r'$'
)

CONTAINER_TYPE_RE = re.compile(
    # e.g.
    #  - list[int]
    #  - dict(str, int)
    #  - dict[str, int]'
    #  - tuple(float, float)
    #  - dict[tuple(str, str), int]'
    r'^'
    r'(dict|list|tuple)'
    r'[\[\(]'
    r'(.+?(?:,\s*)?)+'
    r'[\]\)]'
    r'$'
)

CONTAINER_SPLIT_RE = re.compile(
    # splits dict(str, int) into
    #    ['dict', '[', 'str', ', ', 'int', ']', '']
    r'(\s*[\[\]\(\),]\s*)'
)

DOUBLE_QUOTE_SPLIT_RE = re.compile(
    # splits 'callable ``f(x0, *args)`` or ``f(x0, y0, *args)``' into
    #    ['callable ', '``f(x0, *args)``', ' or ', '``f(x0, y0, *args)``', '']
    r'(``.+?``)'
)

IGNORE = {'of', ' of ', 'either', 'or', 'with', 'in', 'default'}
CONTAINER_CHARS = set('[](){}')


def make_xref_param_type(param_type, xref_aliases):
    """
    Enclose str in a role that creates a cross-reference

    The role ``xref_param_type`` *may be* added to any token
    that looks like type information and no other. The
    function tries to be clever and catch type information
    in different disguises.

    Parameters
    ----------
    param_type : str
        text
    xref_aliases : dict
        Mapping used to resolve common abbreviations and aliases
        to fully qualified names that can be cross-referenced.

    Returns
    -------
    out : str
        Text with parts that may be wrapped in a
        ``xref_param_type`` role.
    """
    if param_type in xref_aliases:
        param_type = xref_aliases[param_type]

    if (QUALIFIED_NAME_RE.match(param_type) and
            param_type not in IGNORE):
        return ':xref_param_type:`%s`' % param_type

    # Clever stuff below (except the last return)
    # can be removed without affecting the basic functionality.

    def _split_and_apply_re(s, pattern):
        """
        Split string using the regex pattern,
        apply main function to the parts that do not match the pattern,
        combine the results
        """
        results = []
        tokens = pattern.split(s)
        if len(tokens) > 1:
            for tok in tokens:
                if pattern.match(tok):
                    results.append(tok)
                else:
                    results.append(
                        make_xref_param_type(tok, xref_aliases))

            return ''.join(results)
        return s

    def _split_and_apply_str(s, on):
        """
        Split string s, at the substring on,
        apply main function to the splits,
        combine the results
        """
        return on.join(
            make_xref_param_type(s, xref_aliases)
            for s in s.split(on))

    # The cases are dealt with in an order the prevents
    # conflict.
    # Then the strategy is:
    #   - Identify a pattern we are not interested in
    #   - split off the pattern
    #   - re-apply the function to the other parts
    #   - join the results with the pattern

    # endswith ', optional'
    if param_type.endswith(', optional'):
        return '%s, optional' % make_xref_param_type(
            param_type[:-10],
            xref_aliases)

    # Any sort of bracket '[](){}'
    has_container = any(c in CONTAINER_CHARS for c in param_type)
    if has_container:
        # of the form 'dict[int, float]'
        if CONTAINER_TYPE_RE.match(param_type):
            return _split_and_apply_re(param_type, CONTAINER_SPLIT_RE)
        else:
            # of the form '[int, float]'
            for start, end in ['[]', '()', '{}']:
                if param_type.startswith(start) and param_type.endswith(end):
                    return '%s%s%s' % (
                        start,
                        make_xref_param_type(param_type[1:-1], xref_aliases),
                        end)

    # May have an unsplittable literal
    if '``' in param_type:
        return _split_and_apply_re(param_type, DOUBLE_QUOTE_SPLIT_RE)

    # Is splittable
    for splitter in [' or ', ', ', ' ']:
        if splitter in param_type:
            return _split_and_apply_str(param_type, splitter)

    return param_type


def xref_param_type_role(role, rawtext, text, lineno, inliner,
                         options={}, content=[]):
    """
    Add a pending_xref for the param_type of a field list
    """
    if text.startswith(('~', '.')):
        prefix, target = text[0], text[1:]
        if prefix == '.':
            env = inliner.document.settings.env
            modname = env.ref_context.get('py:module')
            text = text[1:]
            target = '%s.%s' % (modname, text)
        elif prefix == '~':
            text = text.split('.')[-1]
    else:
        target = text

    contnode = addnodes.literal_emphasis(text, text)
    node = addnodes.pending_xref('', refdomain='py', refexplicit=False,
                                 reftype='obj', reftarget=target)
    node += contnode
    return [node], []
