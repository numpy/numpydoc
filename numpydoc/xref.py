import re

from docutils import nodes
from sphinx import addnodes
from sphinx.util.nodes import split_explicit_title

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

# Note: we never split on commas that are not followed by a space
# You risk creating bad rst markup if you do so.

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
    r'(\s*[\[\]\(\)\{\}]\s*|,\s+)'
)

CONTAINER_SPLIT_REJECT_RE = re.compile(
    # Leads to bad markup e.g.
    # {int}qualified_name
    r'[\]\)\}]\w'
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

SINGLE_QUOTE_SPLIT_RE = re.compile(
    # splits to preserve quoted expressions roles
    r'(`.+?`)'
)

TEXT_SPLIT_RE = re.compile(
    # splits on ' or ', ' | ', ', ' and ' '
    r'(\s+or\s+|\s+\|\s+|,\s+|\s+)'
)

CONTAINER_CHARS = set('[](){}')


def make_xref_param_type(param_type, xref_aliases, xref_ignore):
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
    xref_ignore : set
        Words not to cross-reference.

    Returns
    -------
    out : str
        Text with parts that may be wrapped in a
        ``xref_param_type`` role.
    """
    if param_type in xref_aliases:
        link, title = xref_aliases[param_type], param_type
        param_type = link
    else:
        link = title = param_type

    if QUALIFIED_NAME_RE.match(link) and link not in xref_ignore:
        if link != title:
            return ':xref_param_type:`%s <%s>`' % (title, link)
        else:
            return ':xref_param_type:`%s`' % link

    def _split_and_apply_re(s, pattern):
        """
        Split string using the regex pattern,
        apply main function to the parts that do not match the pattern,
        combine the results
        """
        results = []
        tokens = pattern.split(s)
        n = len(tokens)
        if n > 1:
            for i, tok in enumerate(tokens):
                if pattern.match(tok):
                    results.append(tok)
                else:
                    res = make_xref_param_type(
                        tok, xref_aliases, xref_ignore)
                    # Openning brackets immediated after a role is
                    # bad markup. Detect that and add backslash.
                    # :role:`type`( to :role:`type`\(
                    if res and res[-1] == '`' and i < n-1:
                        next_char = tokens[i+1][0]
                        if next_char in '([{':
                            res += '\\'
                    results.append(res)

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

    # Any quoted expressions
    if '`' in param_type:
        return _split_and_apply_re(param_type, SINGLE_QUOTE_SPLIT_RE)

    # Any sort of bracket '[](){}'
    if any(c in CONTAINER_CHARS for c in param_type):
        if CONTAINER_SPLIT_REJECT_RE.search(param_type):
            return param_type
        return _split_and_apply_re(param_type, CONTAINER_SPLIT_RE)

    # Common splitter tokens
    return _split_and_apply_re(param_type, TEXT_SPLIT_RE)


def xref_param_type_role(role, rawtext, text, lineno, inliner,
                         options={}, content=[]):
    """
    Add a pending_xref for the param_type of a field list
    """
    has_title, title, target = split_explicit_title(text)
    if has_title:
        target = target.lstrip('~')
    else:
        if target.startswith(('~', '.')):
            prefix, target = target[0], target[1:]
            if prefix == '.':
                env = inliner.document.settings.env
                modname = env.ref_context.get('py:module')
                target = target[1:]
                target = '%s.%s' % (modname, target)
            elif prefix == '~':
                title = target.split('.')[-1]

    contnode = nodes.Text(title, title)
    node = addnodes.pending_xref('', refdomain='py', refexplicit=False,
                                 reftype='class', reftarget=target)
    node += contnode
    return [node], []
