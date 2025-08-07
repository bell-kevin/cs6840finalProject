"""Simple benchmarking script comparing BDD and explicit CTL checkers."""

from __future__ import annotations

import os
import sys
import time
import tracemalloc

# Allow running the script directly from the repository root
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.bddctl import TransitionSystem, CTLModelChecker
from src.explicitctl import ExplicitTransitionSystem, ExplicitCTLModelChecker


def build_ring(n: int):
    transitions = [(i, (i + 1) % n) for i in range(n)]
    labeling = {n // 2: {"p"}}
    return transitions, labeling


def run_checker(checker, formula: str):
    start = time.perf_counter()
    tracemalloc.start()
    res = checker.satisfies(formula)
    mem_curr, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end = time.perf_counter()
    return res, end - start, mem_peak / 1024.0  # return time and peak KB


def main() -> None:
    formula = "AF p"
    for n in [20, 200, 1000]:
        transitions, labeling = build_ring(n)

        ts_bdd = TransitionSystem(num_states=n, transitions=transitions, labeling=labeling, init={0})
        ts_exp = ExplicitTransitionSystem(num_states=n, transitions=transitions, labeling=labeling, init={0})

        bdd_mc = CTLModelChecker(ts_bdd)
        exp_mc = ExplicitCTLModelChecker(ts_exp)

        res_bdd, time_bdd, mem_bdd = run_checker(bdd_mc, formula)
        res_exp, time_exp, mem_exp = run_checker(exp_mc, formula)

        print(f"n={n} BDD result: {res_bdd} time: {time_bdd:.4f}s peak KB: {mem_bdd:.1f}")
        print(f"n={n} Explicit result: {res_exp} time: {time_exp:.4f}s peak KB: {mem_exp:.1f}")
        print()


if __name__ == "__main__":
    main()
