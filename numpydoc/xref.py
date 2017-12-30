import re
from sphinx import addnodes

# When sphinx (including the napoleon extension) parses the parameters
# section of a docstring, it converts the information into field lists.
# Some items in the list are for the parameter type. When the type fields
# are processed, the text is split and some tokens are turned into
# pending_xref nodes. These nodes are responsible for creating links.
#
# numpydoc does not create field lists, so the type information is
# not placed into fields that can be processed to make links. Instead,
# when parsing the type information we identify tokens that are link
# worthy and wrap them around a special role (xref_param_type_role).
# When the role is processed, we create pending_xref nodes which are
# later turned into links.


QUALIFIED_NAME_RE = re.compile(
    # e.g int, numpy.array, ~numpy.array, .class_in_current_module
    r'^'
    r'[~\.]?'
    r'[a-zA-Z_]\w*'
    r'(?:\.[a-zA-Z_]\w*)*'
    r'$'
)

CONTAINER_SPLIT_RE = re.compile(
    # splits dict(str, int) into
    #    ['dict', '[', 'str', ', ', 'int', ']', '']
    r'(\s*[\[\]\(\)\{\},]\s*)'
)

DOUBLE_QUOTE_SPLIT_RE = re.compile(
    # splits 'callable ``f(x0, *args)`` or ``f(x0, y0, *args)``' into
    #    ['callable ', '``f(x0, *args)``', ' or ', '``f(x0, y0, *args)``', '']
    r'(``.+?``)'
)

ROLE_SPLIT_RE = re.compile(
    # splits to preserve ReST roles
    r'(:\w+:`.+?(?<!\\)`)'
)

TEXT_SPLIT_RE = re.compile(
    # splits on ' or ', ' | ', ', ' and ' '
    r'(\s+or\s+|\s+\|\s+|,\s+|\s+)'
)

IGNORE = {'of', 'either', 'or', 'with', 'in', 'default', 'optional'}
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

    # The cases are dealt with in an order the prevents
    # conflict.
    # Then the strategy is:
    #   - Identify a pattern we are not interested in
    #   - split off the pattern
    #   - re-apply the function to the other parts
    #   - join the results with the pattern

    # Unsplittable literal
    if '``' in param_type:
        return _split_and_apply_re(param_type, DOUBLE_QUOTE_SPLIT_RE)

    # Any roles
    if ':`' in param_type:
        return _split_and_apply_re(param_type, ROLE_SPLIT_RE)

    # Any sort of bracket '[](){}'
    if any(c in CONTAINER_CHARS for c in param_type):
        return _split_and_apply_re(param_type, CONTAINER_SPLIT_RE)

    # Common splitter tokens
    return _split_and_apply_re(param_type, TEXT_SPLIT_RE)


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
                                 reftype='class', reftarget=target)
    node += contnode
    return [node], []
