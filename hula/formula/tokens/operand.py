import regex
import schedula as sh
from . import Token
from ..exceptions import TokenError
from .parenthesis import _update_n_args
import numpy as np


class XlError(sh.Token):
    pass


class Operand(Token):
    def ast(self, tokens, stack, builder):
        if tokens and isinstance(tokens[-1], Operand):
            raise TokenError()
        super(Operand, self).ast(tokens, stack, builder)
        builder.append(self)
        _update_n_args(stack)


class String(Operand):
    _re = regex.compile(r"""^\s*"(?P<name>(?>""|[^"])*)"\s*|^\s*'(?P<name>(?>''|[^'])*)'\s*""")

    def compile(self):
        return self.name.replace('""', '"').replace("''", "'")

    def set_expr(self, *tokens):
        self.attr['expr'] = '"%s"' % self.name


class Empty(Operand):
    def __init__(self):
        self.source, self.attr = None, {'name': ''}

    @staticmethod
    def compile():
        return 0


_re_error = regex.compile(r'''
    ^\s*(?>
        (?>
            '(\[(?>[^\[\]]+)\])?
            (?>(?>''|[^\?!*\/\[\]':"])+)?'
        |
            (\[(?>[0-9]+)\])(?>(?>''|[^\?!*\/\[\]':"])+)?
        |
            (?>[^\W\d][\w\.]*)
        |
            '(?>(?>''|[^\?!*\/\[\]':"])+)'
        )!
    )?(?P<name>\#(?>NULL!|DIV/0!|VALUE!|REF!|NUM!|NAME\?|N/A))\s*
''', regex.IGNORECASE | regex.X | regex.DOTALL)


class Error(Operand):
    _re = _re_error
    errors = {
        "#NULL!": None,
        "#N/A": np.nan,
        "#NAME?": None,
        "#NUM!": np.nan,
        "#REF!": None,
        "#VALUE!": np.nan,
        "#DIV/0!": np.nan,

    }

    def compile(self):
        return self.errors[self.name]


class Number(Operand):
    _re = regex.compile(
        r'^\s*(?P<name>[0-9]+(?>\.[0-9]+)?(?>E[+-][0-9]+)?|'
        r'TRUE(?!\(\))|FALSE(?!\(\)))(?!([a-z]|[0-9]|\.|\s*\:))\s*',
        regex.IGNORECASE
    )

    def compile(self):
        return eval(self.name.capitalize())


class Column(Operand):
    _re = regex.compile(
        r'^(?P<name>[\u4E00-\u9FA5A-Za-z0-9_]+)(?P<raise>[\(\.]?)',
        regex.IGNORECASE | regex.X | regex.DOTALL
    )

    def process(self, match, context=None):
        return super(Column, self).process(match, context)

    def __repr__(self):
        if self.attr.get('is_ranges', False):
            return '{} <{}>'.format(self.name, Column.__name__)
        else:
            return '{} <{}>'.format(self.name, Column.__name__)

    def compile(self):
        if self.df is None:
            raise TokenError
        if self.name not in self.df.columns:
            raise TokenError
        return self.df[self.name]
