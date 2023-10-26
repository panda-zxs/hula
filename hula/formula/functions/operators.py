import functools
import collections
from . import (
    replace_empty, not_implemented, wrap_func, wrap_ufunc, Error, value_return
)
from .text import _str

OPERATORS = collections.defaultdict(lambda: not_implemented)

numeric_wrap = functools.partial(wrap_ufunc, return_func=value_return)

OPERATORS.update({k: numeric_wrap(v) for k, v in {
    '+': lambda x, y: float(x) + float(y),
    '-': lambda x, y: float(x) - float(y),
    'U-': lambda x: -float(x),
    '*': lambda x, y: float(x) * float(y),
    '/': lambda x, y: (float(x) / float(y)) if y else Error.errors['#DIV/0!'],
    '^': lambda x, y: float(x) ** float(y),
    '%': lambda x: float(x) / 100.0,
}.items()})
OPERATORS['U+'] = wrap_ufunc(
    lambda x: x, input_parser=lambda *a: a, return_func=value_return
)

LOGIC_OPERATORS = collections.OrderedDict([
    ('>=', lambda x, y: x >= y),
    ('<=', lambda x, y: x <= y),
    ('<>', lambda x, y: x != y),
    ('<', lambda x, y: x < y),
    ('>', lambda x, y: x > y),
    ('=', lambda x, y: x == y),
])
OPERATORS.update({k: v for k, v in LOGIC_OPERATORS.items()})
OPERATORS['&'] = wrap_ufunc(
    lambda x, y: x + y, input_parser=lambda *a: map(_str, a),
    args_parser=lambda *a: (replace_empty(v, '') for v in a),
    return_func=value_return
)
OPERATORS.update({k: wrap_func(v, ranges=True) for k, v in {
    ',': lambda x, y: x | y,
    ' ': lambda x, y: x & y,
    ':': lambda x, y: x + y
}.items()})
