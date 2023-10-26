import math
import functools
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
from . import (
    wrap_ufunc, wrap_func, Error,
)

FUNCTIONS = {}


def xceiling(num, sig, ceil=math.ceil, dfl=0):
    if sig == 0:
        return dfl
    elif sig < 0 < num:
        return np.nan
    return ceil(num / sig) * sig


def xceiling_math(num, sig=None, mode=0, ceil=math.ceil):
    if sig == 0:
        return 0
    elif sig is None:
        x, sig = abs(num), 1
    else:
        sig = abs(sig)
        x = num / sig
    if mode and num < 0:
        return -ceil(abs(x)) * sig
    return ceil(x) * sig


def xeven(x):
    v = math.ceil(abs(x) / 2.) * 2
    return -v if x < 0 else v


def _factdouble(x):
    return np.multiply.reduce(np.arange(max(x, 1), 0, -2))


def xpower(number, power):
    if number == 0:
        if power == 0:
            return Error.errors['#NUM!']
        if power < 0:
            return Error.errors['#DIV/0!']
    return np.power(number, power)


def round_up(x):
    return float(Decimal(x).quantize(0, rounding=ROUND_HALF_UP))


def xround(x, d, func=round_up):
    d = 10 ** int(d)
    v = func(abs(x * d)) / d
    return -v if x < 0 else v


def xsum(*args):
    _args = []
    _series = []
    rst = None
    for i in args:
        if not isinstance(i, pd.Series):
            _args.append(i)
        else:
            _series.append(i)
    if _series:
        r_series = _series[0]
        for i in _series[1:]:
            r_series += i
        rst = r_series
    if _args:
        r_n = sum(_args)
        if rst is not None:
            rst = rst + r_n
        else:
            rst = r_n
    if rst is None:
        raise ValueError
    if not isinstance(rst, pd.Series):
        if isinstance(rst, int):
            return pd.Series([rst], dtype=int)
        elif isinstance(rst, float):
            return pd.Series([rst], dtype=float)
    return rst


def xint(v):
    if isinstance(v, pd.Series):
        return v.astype(int)
    else:
        return int(v)


def xavg(v):
    if isinstance(v, pd.Series):
        try:
            return v.mean()
        except TypeError:
            return np.nan
    else:
        return v


def xisnan(v):
    return np.isnan(v)


FUNCTIONS['ABS'] = wrap_ufunc(np.abs)
FUNCTIONS['CEILING'] = wrap_ufunc(xceiling)
FUNCTIONS['CEILING.MATH'] = wrap_ufunc(xceiling_math)
FUNCTIONS['DEGREES'] = wrap_ufunc(np.degrees)
FUNCTIONS['EVEN'] = wrap_ufunc(xeven)
FUNCTIONS['EXP'] = wrap_ufunc(np.exp)
FUNCTIONS['FLOOR'] = wrap_ufunc(functools.partial(xceiling, ceil=math.floor, dfl=Error.errors['#DIV/0!']))
FUNCTIONS['INT'] = wrap_ufunc(xint)
FUNCTIONS['LOG10'] = wrap_ufunc(np.log10)
FUNCTIONS['LOG'] = wrap_ufunc(lambda x, base=10: np.log(x) / np.log(base) if base else np.nan)
FUNCTIONS['LN'] = wrap_ufunc(np.log)
FUNCTIONS['POWER'] = wrap_ufunc(xpower)
FUNCTIONS['ROUND'] = wrap_ufunc(xround)
FUNCTIONS['ROUNDDOWN'] = wrap_ufunc(functools.partial(xround, func=math.floor))
FUNCTIONS['ROUNDUP'] = wrap_ufunc(functools.partial(xround, func=math.ceil))
FUNCTIONS['SUM'] = wrap_func(xsum)
FUNCTIONS['AVG'] = wrap_func(xavg)
FUNCTIONS['ISNAN'] = wrap_func(xisnan)
