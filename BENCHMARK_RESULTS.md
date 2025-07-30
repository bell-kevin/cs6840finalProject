# Benchmark Results

This document summarizes a brief performance comparison between the BDD-based and explicit-state CTL model checkers.

Benchmarks were executed on the default container environment using Python 3.12. The results below were produced by running the scripts in the `benchmarks/` directory.

## Ring Topology

`run_benchmarks.py` constructs a ring of 20 states and checks `AF p` with both backends:

```
$ python benchmarks/run_benchmarks.py
BDD result: True time: 0.0280s peak KB: 326.7
Explicit result: True time: 0.0009s peak KB: 7.0
```

The explicit checker is faster on this tiny example, but consumes similar peak memory.

## Variable Ordering

`variable_order.py` explores the impact of BDD variable ordering for a chain of 16 states:

```
$ python benchmarks/variable_order.py
Default order: True time: 0.0035s
Reversed order: True time: 0.0026s
```

For this small system both orders yield the same result and comparable runtime, but larger models may show greater differences.
