"""Experiment demonstrating impact of BDD variable ordering."""

from __future__ import annotations

import os
import sys
import time
import math

# Allow running the script directly from the repository root
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.bddctl import TransitionSystem, CTLModelChecker


def build_chain(n: int):
    transitions = [(i, i + 1) for i in range(n - 1)]
    transitions.append((n - 1, n - 1))
    labeling = {n - 1: {"p"}}
    return transitions, labeling


def run_with_order(n: int, order):
    transitions, labeling = build_chain(n)
    ts = TransitionSystem(num_states=n, transitions=transitions, labeling=labeling, init={0}, var_order=order)
    mc = CTLModelChecker(ts)
    start = time.perf_counter()
    res = mc.satisfies("AF p")
    elapsed = time.perf_counter() - start
    return res, elapsed


def main() -> None:
    for n in [16, 64]:
        default_res, default_time = run_with_order(n, None)
        n_bits = int(math.ceil(math.log2(n))) or 1
        reverse_order = list(reversed(range(n_bits)))
        rev_res, rev_time = run_with_order(n, reverse_order)

        print(f"n={n} default order: {default_res} time: {default_time:.4f}s")
        print(f"n={n} reversed order: {rev_res} time: {rev_time:.4f}s")
        print()


if __name__ == "__main__":
    main()
