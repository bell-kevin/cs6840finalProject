from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Set, Tuple, List, Any

from dd.autoref import BDD
import warnings
# Suppress deprecation warnings triggered by lark's use of `sre_parse` and
# `sre_constants`. The library still imports these modules on Python 3.12,
# which causes noisy `DeprecationWarning` messages during test runs.
warnings.filterwarnings(
    "ignore",
    "module 'sre_parse' is deprecated",
    DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    "module 'sre_constants' is deprecated",
    DeprecationWarning,
)
from lark import Lark, Transformer, v_args


class CTLParser(Transformer):
    def start(self, args):
        return args[0]

    def or_expr(self, args):
        left, right = args
        return ('or', left, right)

    def and_expr(self, args):
        left, right = args
        return ('and', left, right)

    def not_expr(self, args):
        (child,) = args
        return ('not', child)

    def ex_expr(self, args):
        (child,) = args
        return ('ex', child)

    def ax_expr(self, args):
        (child,) = args
        return ('ax', child)

    def ef_expr(self, args):
        (child,) = args
        return ('ef', child)

    def af_expr(self, args):
        (child,) = args
        return ('af', child)

    def eg_expr(self, args):
        (child,) = args
        return ('eg', child)

    def ag_expr(self, args):
        (child,) = args
        return ('ag', child)

    def eu_expr(self, args):
        left, right = args
        return ('eu', left, right)

    def au_expr(self, args):
        left, right = args
        return ('au', left, right)

    def atom(self, args):
        token = args[0]
        return ('atom', str(token))


grammar = r"""
?start: expr
?expr: or
?or: and
    | or "OR" and       -> or_expr
?and: unary
    | and "AND" unary    -> and_expr
?unary: "NOT" unary      -> not_expr
      | "EX" unary       -> ex_expr
      | "AX" unary       -> ax_expr
      | "EF" unary       -> ef_expr
      | "AF" unary       -> af_expr
      | "EG" unary       -> eg_expr
      | "AG" unary       -> ag_expr
      | eu
      | au
      | "(" expr ")"      -> group
      | atom

eu: "E" "[" expr "U" expr "]"  -> eu_expr
au: "A" "[" expr "U" expr "]"  -> au_expr
atom: /[a-zA-Z_][a-zA-Z0-9_]*/
%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start', parser='lalr', transformer=CTLParser())


def parse_ctl(text: str):
    return parser.parse(text)


@dataclass
class TransitionSystem:
    num_states: int
    transitions: List[Tuple[int, int]]
    labeling: Dict[int, Set[str]]
    init: Set[int] | None = None
    var_order: List[int] | None = None

    def __post_init__(self):
        if self.init is None:
            self.init = set(range(self.num_states))
        self.num_bits = max(1, math.ceil(math.log2(self.num_states)))
        self.bdd = BDD()
        self.state_vars = [f"s{i}" for i in range(self.num_bits)]
        self.next_vars = [f"s{i}_next" for i in range(self.num_bits)]
        order = self.state_vars + self.next_vars
        if self.var_order is not None:
            if sorted(self.var_order) != list(range(self.num_bits)):
                raise ValueError("var_order must be a permutation of bit indices")
            order = [self.state_vars[i] for i in self.var_order] + [
                self.next_vars[i] for i in self.var_order
            ]
        self.bdd.declare(*order)
        self.var_map = {v: vp for v, vp in zip(self.state_vars, self.next_vars)}
        self.var_map_inv = {vp: v for v, vp in zip(self.state_vars, self.next_vars)}
        self._build_transition_relation()

    def _build_transition_relation(self):
        bdd = self.bdd
        T = bdd.false
        for u, v in self.transitions:
            cu = self.state_bdd(u)
            cv = self._prime(self.state_bdd(v))
            T |= cu & cv
        self.T = T

    def state_bdd(self, state: int):
        bdd = self.bdd
        assert 0 <= state < self.num_states
        bits = self.state_vars
        result = bdd.true
        for i, var in enumerate(bits):
            bit = (state >> i) & 1
            if bit:
                result &= bdd.var(var)
            else:
                result &= ~bdd.var(var)
        return result

    def _prime(self, node):
        return self.bdd.let(self.var_map, node)

    def _unprime(self, node):
        return self.bdd.let(self.var_map_inv, node)

    def ap_bdd(self, ap: str):
        result = self.bdd.false
        for s in range(self.num_states):
            if ap in self.labeling.get(s, set()):
                result |= self.state_bdd(s)
        return result

    def pre(self, X):
        prime_X = self._prime(X)
        tmp = self.T & prime_X
        res = self.bdd.exist(self.next_vars, tmp)
        return res

    def post(self, X):
        prime = self.bdd.exist(self.state_vars, self._prime(X) & self.T)
        return self._unprime(prime)


class CTLModelChecker:
    def __init__(self, ts: TransitionSystem):
        self.ts = ts
        self.bdd = ts.bdd

    def eval(self, node):
        kind = node[0]
        if kind == 'atom':
            return self.ts.ap_bdd(node[1])
        if kind == 'not':
            return ~self.eval(node[1])
        if kind == 'and':
            return self.eval(node[1]) & self.eval(node[2])
        if kind == 'or':
            return self.eval(node[1]) | self.eval(node[2])
        if kind == 'ex':
            return self.ts.pre(self.eval(node[1]))
        if kind == 'ax':
            return ~self.ts.pre(~self.eval(node[1]))
        if kind == 'ef':
            return self._least_fix(lambda Y: self.eval(node[1]) | self.ts.pre(Y))
        if kind == 'af':
            return self._least_fix(lambda Y: self.eval(node[1]) | (~self.ts.pre(~Y)))
        if kind == 'eg':
            return self._greatest_fix(lambda Y: self.eval(node[1]) & self.ts.pre(Y))
        if kind == 'ag':
            return self._greatest_fix(lambda Y: self.eval(node[1]) & (~self.ts.pre(~Y)))
        if kind == 'eu':
            phi, psi = node[1], node[2]
            return self._least_fix(lambda Y: self.eval(psi) | (self.eval(phi) & self.ts.pre(Y)))
        if kind == 'au':
            phi, psi = node[1], node[2]
            return self._least_fix(lambda Y: self.eval(psi) | (self.eval(phi) & (~self.ts.pre(~Y))))
        raise ValueError(f"Unknown node kind {kind}")

    def _least_fix(self, func):
        bdd = self.bdd
        Y = bdd.false
        while True:
            new = func(Y)
            if new == Y:
                return Y
            Y = new

    def _greatest_fix(self, func):
        bdd = self.bdd
        Y = bdd.true
        while True:
            new = func(Y)
            if new == Y:
                return Y
            Y = new

    def satisfies(self, formula):
        ast = parse_ctl(formula) if isinstance(formula, str) else formula
        result_bdd = self.eval(ast)
        init_states = self.bdd.false
        for s in self.ts.init:
            init_states |= self.ts.state_bdd(s)
        return init_states <= result_bdd


__all__ = ["TransitionSystem", "CTLModelChecker", "parse_ctl"]
