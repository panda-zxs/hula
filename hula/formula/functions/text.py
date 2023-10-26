import functools
import re
import pandas as pd

from . import (
    wrap_ufunc, Error, replace_empty, XlError, value_return, wrap_func,
)

FUNCTIONS = {}


def _str(text):
    if isinstance(text, bool):
        return str(text).upper()
    if isinstance(text, float) and text.is_integer():
        return '%d' % text
    return str(text)


def xfind(find_text, within_text, start_num=1):
    i = int(start_num or 0) - 1
    res = i >= 0 and _str(within_text).find(_str(find_text), i) + 1 or 0
    return res or Error.errors['#VALUE!']


_kw0 = {
    'input_parser': lambda *a: a,
    'args_parser': lambda *a: map(functools.partial(replace_empty, empty=''), a)
}


def xleft(from_str, num_chars):
    i = int(num_chars or 0)
    if i >= 0:
        return _str(from_str)[:i]
    return Error.errors['#VALUE!']


_kw1 = {
    'input_parser': lambda text: [_str(text)], 'return_func': value_return,
    'args_parser': lambda *a: map(functools.partial(replace_empty, empty=''), a)
}


def xmid(from_str, start_num, num_chars):
    i = j = int(start_num or 0) - 1
    j += int(num_chars or 0)
    if 0 <= i <= j:
        return _str(from_str)[i:j]
    return Error.errors['#VALUE!']


def xreplace(old_text, start_num, num_chars, new_text):
    old_text, new_text = _str(old_text), _str(new_text)
    i = j = int(start_num or 0) - 1
    j += int(num_chars or 0)
    if 0 <= i <= j:
        return old_text[:i] + new_text + old_text[j:]
    return Error.errors['#VALUE!']


def xsubstitute(sr, old_text, new_text, i=1, n=None):
    sr = str(sr)
    idx = sr.index(old_text, i - 1)
    if n is None:
        return sr[:idx] + re.sub(old_text, new_text, sr[idx:])
    else:
        return sr[:idx] + re.sub(old_text, new_text, sr[idx:], count=n)


def xright(from_str, num_chars):
    res = xleft(_str(from_str)[::-1], num_chars)
    return res if isinstance(res, XlError) else res[::-1]


def xconcat(*args):
    rst = args[0]
    if isinstance(rst, pd.Series):
        if rst.dtype != "object":
            rst = rst.astype(str)
    else:
        rst = str(rst)
    for arg in args[1:]:
        if isinstance(arg, pd.Series):
            arg = arg.astype(str)
        else:
            arg = str(arg)

        rst += arg
    return rst


def xtext(sr, fm):
    return format(float(sr), fm)


def xvalue(sr):
    return float(sr)


def xisnull(sr):
    return sr is None


FUNCTIONS['CONCAT'] = wrap_func(xconcat)
FUNCTIONS['LEN'] = wrap_ufunc(str.__len__, **_kw1)
FUNCTIONS['UPPER'] = wrap_ufunc(str.upper, **_kw1)
FUNCTIONS['LOWER'] = wrap_ufunc(str.lower, **_kw1)
FUNCTIONS['PROPER'] = wrap_ufunc(str.capitalize, **_kw1)
FUNCTIONS['MID'] = wrap_ufunc(xmid, **_kw0)
FUNCTIONS['LEFT'] = wrap_ufunc(xleft, **_kw0)
FUNCTIONS['RIGHT'] = wrap_ufunc(xright, **_kw0)
FUNCTIONS['REPLACE'] = wrap_ufunc(xreplace, **_kw0)
FUNCTIONS['SUBSTITUTE'] = wrap_ufunc(xsubstitute, **_kw0)
FUNCTIONS['TEXT'] = wrap_ufunc(xtext, **_kw0)
FUNCTIONS['VALUE'] = wrap_ufunc(xvalue, **_kw0)
FUNCTIONS['ISNULL'] = wrap_ufunc(xisnull, **_kw0)
