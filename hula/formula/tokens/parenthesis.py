from . import Token
from ..exceptions import ParenthesesError, TokenError

import regex


class Parenthesis(Token):
    _re = regex.compile(
        r'^\s*(?>(?P<name>(?P<start>\())\s*|(?P<name>(?P<end>\))))'
    )

    opens = {')': '('}
    # 参数个数
    n_args = 0

    # 语法解析处理
    def ast(self, tokens, stack, builder):
        # 校验
        from .operand import Operand
        if self.has_start and tokens and isinstance(tokens[-1], Operand):
            raise TokenError
        # 添加实例到 tokens 队列
        super(Parenthesis, self).ast(tokens, stack, builder)
        # 如果实例是( 添加实例到堆栈
        if self.has_start:
            stack.append(self)
            self.attr['check_n'] = self.attr.get('check_n', lambda t: t.n_args)
        else:
            # 批量弹出堆栈并加入 builder 队列直到遇到(停止
            while stack and not stack[-1].has_start:
                builder.append(stack.pop())

            if not stack or self.opens[self.name] != stack[-1].name:
                raise ParenthesesError()
            token = stack.pop()
            if not token.get_check_n(token):
                raise ParenthesesError()
            n = self.attr['n_args'] = token.n_args
            from .function import Function
            # 如果堆栈最后一个是函数则弹出, 加入builder
            if stack and isinstance(stack[-1], Function):
                stack[-1].attr['n_args'] = token.n_args
                builder.append(stack.pop())
            elif n > 1:
                # 如果入参大于1, 将参数加入 builder 队列
                from .operator import Separator
                for i in range(n - 1):
                    builder.append(Separator(','))
            _update_n_args(stack)


# (后面入参计数
def _update_n_args(stack):
    if stack:
        t = stack[-1]
        if isinstance(t, Parenthesis) and t.has_start:
            t.n_args += 1
