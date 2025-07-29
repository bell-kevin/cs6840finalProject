"""Experiment demonstrating impact of BDD variable ordering."""

from __future__ import annotations

import time

from src.bddctl import TransitionSystem, CTLModelChecker
import math


def build_chain(n: int):
    transitions = [(i, i + 1) for i in range(n - 1)]
    transitions.append((n - 1, n - 1))
    labeling = {n - 1: {"p"}}
    return transitions, labeling


def run_with_order(order):
    n = 16
    transitions, labeling = build_chain(n)
    ts = TransitionSystem(num_states=n, transitions=transitions, labeling=labeling, init={0}, var_order=order)
    mc = CTLModelChecker(ts)
    start = time.perf_counter()
    res = mc.satisfies("AF p")
    elapsed = time.perf_counter() - start
    return res, elapsed


def main() -> None:
    default_res, default_time = run_with_order(None)
    n_bits = int(math.ceil(math.log2(16))) or 1
    reverse_order = list(reversed(range(n_bits)))
    rev_res, rev_time = run_with_order(reverse_order)

    print("Default order:", default_res, "time: %.4fs" % default_time)
    print("Reversed order:", rev_res, "time: %.4fs" % rev_time)


if __name__ == "__main__":
    main()
