# Benchmark Results

This document summarizes a brief performance comparison between the BDD-based and explicit-state CTL model checkers.

Benchmarks were executed on the default container environment using Python 3.12. The results below were produced by running the scripts in the `benchmarks/` directory.

## Ring Topology

`run_benchmarks.py` constructs rings of increasing size and checks `AF p` with both backends:

```
$ python benchmarks/run_benchmarks.py
n=20 BDD result: True time: 0.0477s peak KB: 326.7
n=20 Explicit result: True time: 0.0017s peak KB: 7.0

n=200 BDD result: True time: 4.0476s peak KB: 20359.0
n=200 Explicit result: True time: 0.1111s peak KB: 31.8

n=1000 BDD result: True time: 95.6191s peak KB: 409808.0
n=1000 Explicit result: True time: 4.6379s peak KB: 197.5
```

The explicit checker handles larger rings far more efficiently on this workload.

## Variable Ordering

`variable_order.py` explores the impact of BDD variable ordering for chains of 16 and 64 states:

```
$ python benchmarks/variable_order.py
n=16 default order: True time: 0.0059s
n=16 reversed order: True time: 0.0048s

n=64 default order: True time: 0.0940s
n=64 reversed order: True time: 0.0618s
```

Reversing the bit order yields a noticeable speedup for the larger chain, illustrating how variable ordering can affect BDD performance.
