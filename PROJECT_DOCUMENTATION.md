# BDD-Based CTL Model Checker

## Problem Statement
Computational Tree Logic (CTL) model checking explores whether a transition system satisfies temporal formulas describing how propositions evolve over time.  Explicit-state checkers enumerate all reachable states, which often leads to memory blow-up.  This project implements a CTL model checker using Binary Decision Diagrams (BDDs) to encode state sets symbolically.  By representing states and transitions with BDDs, the checker can operate on large systems more efficiently than explicit enumeration.  The goal is to provide a minimal but complete reference implementation that demonstrates fixpoint algorithms with symbolic sets and highlights trade-offs between BDD- and set-based approaches.

## Module Overview

* `src/bddctl.py` – Defines `TransitionSystem`, which builds a symbolic transition relation in the `dd` BDD package, and `CTLModelChecker`, which evaluates CTL formulas via fixpoint computations.  It also contains a small Lark-based parser to turn textual formulas into abstract syntax trees.
* `src/explicitctl.py` – A purely explicit-state counterpart using Python sets.  It mirrors the same `TransitionSystem` and `CTLModelChecker` interface for fair comparisons and easier testing.
* `tests/` – Contains unit tests exercising six representative formulas (`EF`, `AG`, `AF`, `EG`, `E[...]U[...]`, and `A[...]U[...]`).  Tests construct small systems and confirm each backend returns the expected result.
* `benchmarks/` – Two scripts for performance exploration.  `run_benchmarks.py` contrasts runtime and peak memory usage on a ring topology.  `variable_order.py` demonstrates how BDD variable ordering affects a simple chain.
* `example_usage.py` – Runs both model checkers on a tiny system and prints the result of each formula.  This mirrors the README instructions and serves as a quick sanity check.

## Example Workflow
1. Install dependencies with `pip install -r requirements.txt`.
2. Execute `pytest` to ensure all tests pass (twelve in total across both backends).
3. Run `python example_usage.py` to see the output for the sample transition systems.
4. Optionally run the benchmarking scripts to reproduce the timings summarized in `BENCHMARK_RESULTS.md`.

Example output from the usage script:

```
Results of example CTL queries:
BDD EF p: True
BDD AG p: False
BDD AF p: True
BDD EG q: False
BDD E[q U p]: True
BDD A[q U p]: False
Explicit EF p: True
Explicit AG p: False
Explicit AF p: True
Explicit EG q: False
Explicit E[q U p]: True
Explicit A[q U p]: False
```

This documentation, together with the codebase and benchmark results, forms the complete final project submission.
