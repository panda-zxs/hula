from .exceptions import FormulaError, TokenError, ParenthesesError
from .builder import AstBuilder
import regex
from .tokens.parenthesis import Parenthesis
from .tokens.operator import OperatorToken, Separator
from .tokens.operand import String, Error, Number, Column
from .tokens.function import Function


class Parser(object):
    formula_check = regex.compile(
        r"""
        (?P<value>^=\s*(?P<name>\S.*)$)
        """, regex.IGNORECASE | regex.X | regex.DOTALL
    )
    ast_builder = AstBuilder
    # 错误、字符串、数字、列名、运算符、逗号、方法、括号
    filters = [
        Error, String, Number, Column, OperatorToken, Separator, Function, Parenthesis,
    ]

    def __init__(self, df):
        self.df = df

    def is_formula(self, value):
        return bool(self._formula(value)) or False

    def _formula(self, value):
        return self.formula_check.match(value)

    def ast(self, expression, context=None):
        try:
            match = self._formula(expression.replace('\n', '').replace('    ', '')).groupdict()
            expr = match['name']
        except (AttributeError, KeyError):
            raise FormulaError
        builder = self.ast_builder(match=match, df=self.df)
        filters, tokens, stack = self.filters, [], []
        Parenthesis('(').ast(tokens, stack, builder)
        while expr:
            for f in filters:
                try:
                    token = f(expr, context)
                    token.ast(tokens, stack, builder)
                    expr = expr[token.end_match:]
                    break
                except TokenError:
                    pass
                except FormulaError:
                    raise FormulaError(expression)
            else:
                raise FormulaError(expression)
        Parenthesis(')').ast(tokens, stack, builder)
        tokens = tokens[1:-1]
        while stack:
            if isinstance(stack[-1], Parenthesis):
                raise ParenthesesError()
            builder.append(stack.pop())
        if len(builder) != 1:
            raise FormulaError(expression)
        builder.finish()
        return tokens, builder
