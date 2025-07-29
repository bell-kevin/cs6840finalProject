"""Simple benchmarking script comparing BDD and explicit CTL checkers."""

from __future__ import annotations

import time
import tracemalloc

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
    n = 20
    transitions, labeling = build_ring(n)
    formula = "AF p"

    ts_bdd = TransitionSystem(num_states=n, transitions=transitions, labeling=labeling, init={0})
    ts_exp = ExplicitTransitionSystem(num_states=n, transitions=transitions, labeling=labeling, init={0})

    bdd_mc = CTLModelChecker(ts_bdd)
    exp_mc = ExplicitCTLModelChecker(ts_exp)

    res_bdd, time_bdd, mem_bdd = run_checker(bdd_mc, formula)
    res_exp, time_exp, mem_exp = run_checker(exp_mc, formula)

    print("BDD result:", res_bdd, "time: %.4fs" % time_bdd, "peak KB: %.1f" % mem_bdd)
    print("Explicit result:", res_exp, "time: %.4fs" % time_exp, "peak KB: %.1f" % mem_exp)


if __name__ == "__main__":
    main()
