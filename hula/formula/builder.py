import pandas as pd
from schedula import DispatchPipe, Dispatcher, NONE, bypass

from . import functions
from .tokens.operator import Operator
from .tokens.function import Function
from .tokens.operand import Operand, Column
import collections
from .exceptions import RangeValueError, InvalidRangeError, FormulaError
from schedula.utils.utl import get_unused_node_id


class AstBuilder(object):
    compile_class = DispatchPipe

    def __init__(self, dsp=None, nodes=None, match=None, df=None):
        # 双向队列
        self._deque = collections.deque()
        # re结果
        self.match = match
        # 函数工作流
        self.dsp = dsp or Dispatcher(
            raises=lambda e: not isinstance(e, (
                NotImplementedError, RangeValueError, InvalidRangeError
            ))
        )
        self.df = df
        # 工作节点
        self.nodes = nodes or {}
        # 缺少操作数
        self.missing_operands = set()

    def __len__(self):
        return len(self._deque)

    def __getitem__(self, index):
        return self._deque[index]

    def pop(self):
        return self._deque.pop()

    def append(self, token):
        if isinstance(token, (Operator, Function)):
            try:
                tokens = [self.pop() for _ in range(token.get_n_args)][::-1]
            except IndexError:
                raise FormulaError()
            # dsp 添加入参
            token.update_input_tokens(*tokens)
            inputs = [self.get_node_id(i) for i in tokens]
            token.set_expr(*tokens)
            out, dmap, get_id = token.node_id, self.dsp.dmap, get_unused_node_id
            if out not in self.dsp.nodes:
                func = token.compile()
                kw = {
                    'function_id': get_id(dmap, token.name),
                    'function': func,
                    'inputs': inputs or None,
                    'outputs': [out]
                }
                if isinstance(func, dict):
                    _inputs = func.get('extra_inputs', {})
                    for k, v in _inputs.items():
                        if v is not NONE:
                            self.dsp.add_data(k, v)
                    kw['inputs'] = (list(_inputs) + inputs) or None
                    kw.update(func)
                self.dsp.add_function(**kw)
            else:
                self.nodes[token] = n_id = get_id(dmap, out, 'c%d>{}')
                self.dsp.add_function(None, bypass, [out], [n_id])
        elif isinstance(token, Operand):
            self.missing_operands.add(token)
        self._deque.append(token)

    def get_node_id(self, token):
        if token in self.nodes:
            return self.nodes[token]
        if isinstance(token, Operand):
            self.missing_operands.remove(token)
            token.set_expr()
            kw = {}
            if isinstance(token, Column):
                token.set_df(self.df)
            if not token.attr.get('is_reference', False):
                kw['default_value'] = token.compile()
            node_id = self.dsp.add_data(data_id=token.node_id, **kw)
        else:
            node_id = token.node_id
        self.nodes[token] = node_id
        return node_id

    def finish(self):
        for token in list(self.missing_operands):
            self.get_node_id(token)

    def compile(self, references=None, context=None, **inputs):
        dsp, inp = self.dsp, inputs.copy()
        for k, ref in (references or {}).items():
            if k in dsp.data_nodes:
                if isinstance(ref, Column):
                    inp[k] = ref
        res, o = dsp(inp), self.get_node_id(self[-1])
        dsp = dsp.get_sub_dsp_from_workflow(
            [o], graph=dsp.dmap, reverse=True, blockers=res,
            wildcard=False
        )
        dsp.nodes.update({k: v.copy() for k, v in dsp.nodes.items()})

        i = collections.OrderedDict()
        for k in sorted(dsp.data_nodes):
            if not dsp.dmap.pred[k]:
                if k in res:
                    v = res[k]
                    if isinstance(v, functions.Array):
                        v = pd.Series(v)
                    dsp.add_data(data_id=k, default_value=v)
                else:
                    i[k] = None
        dsp.raises = True
        return self.compile_class(
            dsp, '=%s' % o, i, [o], wildcard=False, shrink=False
        )

    def run(self):
        f = self.compile()
        rst = f()
        rst = pd.Series(rst)
        if len(rst) < len(self.df):
            if len(rst) == 1:
                return rst.reindex(range(len(self.df))).fillna(rst[0])
            else:
                return rst.reindex(range(len(self.df)))
        else:
            return rst
