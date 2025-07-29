from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Tuple, List

from .bddctl import parse_ctl


@dataclass
class ExplicitTransitionSystem:
    """Simple explicit-state transition system."""

    num_states: int
    transitions: List[Tuple[int, int]]
    labeling: Dict[int, Set[str]]
    init: Set[int] | None = None

    def __post_init__(self) -> None:
        if self.init is None:
            self.init = set(range(self.num_states))
        self.post_map = {s: set() for s in range(self.num_states)}
        self.pre_map = {s: set() for s in range(self.num_states)}
        for u, v in self.transitions:
            self.post_map.setdefault(u, set()).add(v)
            self.pre_map.setdefault(v, set()).add(u)


class ExplicitCTLModelChecker:
    """Explicit-state CTL model checker using Python sets."""

    def __init__(self, ts: ExplicitTransitionSystem) -> None:
        self.ts = ts

    # ------ helper operations ------
    def pre(self, X: Set[int]) -> Set[int]:
        return {s for s, succ in self.ts.post_map.items() if succ & X}

    # ------ fixpoint utilities ------
    def _least_fix(self, func):
        Y: Set[int] = set()
        while True:
            new = func(Y)
            if new == Y:
                return Y
            Y = new

    def _greatest_fix(self, func):
        Y: Set[int] = set(range(self.ts.num_states))
        while True:
            new = func(Y)
            if new == Y:
                return Y
            Y = new

    # ------ CTL evaluation ------
    def eval(self, node) -> Set[int]:
        kind = node[0]
        if kind == "atom":
            return {s for s in range(self.ts.num_states) if node[1] in self.ts.labeling.get(s, set())}
        if kind == "not":
            return set(range(self.ts.num_states)) - self.eval(node[1])
        if kind == "and":
            return self.eval(node[1]) & self.eval(node[2])
        if kind == "or":
            return self.eval(node[1]) | self.eval(node[2])
        if kind == "ex":
            return self.pre(self.eval(node[1]))
        if kind == "ax":
            return set(range(self.ts.num_states)) - self.pre(set(range(self.ts.num_states)) - self.eval(node[1]))
        if kind == "ef":
            return self._least_fix(lambda Y: self.eval(node[1]) | self.pre(Y))
        if kind == "af":
            return self._least_fix(lambda Y: self.eval(node[1]) | (set(range(self.ts.num_states)) - self.pre(set(range(self.ts.num_states)) - Y)))
        if kind == "eg":
            return self._greatest_fix(lambda Y: self.eval(node[1]) & self.pre(Y))
        if kind == "ag":
            return self._greatest_fix(lambda Y: self.eval(node[1]) & (set(range(self.ts.num_states)) - self.pre(set(range(self.ts.num_states)) - Y)))
        if kind == "eu":
            phi, psi = node[1], node[2]
            return self._least_fix(lambda Y: self.eval(psi) | (self.eval(phi) & self.pre(Y)))
        if kind == "au":
            phi, psi = node[1], node[2]
            return self._least_fix(lambda Y: self.eval(psi) | (self.eval(phi) & (set(range(self.ts.num_states)) - self.pre(set(range(self.ts.num_states)) - Y))))
        raise ValueError(f"Unknown node kind {kind}")

    def satisfies(self, formula) -> bool:
        ast = parse_ctl(formula) if isinstance(formula, str) else formula
        result = self.eval(ast)
        return self.ts.init <= result


__all__ = ["ExplicitTransitionSystem", "ExplicitCTLModelChecker"]
