<a name="readme-top"></a>

# BDD-Based CTL Model Checker

A Python implementation of a Computation Tree Logic (CTL) model checker that
represents state sets symbolically using Binary Decision Diagrams (BDDs). A
reference explicit-state checker is included for comparison and benchmarking.

## Table of Contents
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Example Usage](#example-usage)
- [C Implementation](#c-implementation)
- [Benchmarks](#benchmarks)
- [Documentation](#documentation)

## Getting Started

The project requires **Python 3.10+**. Source code lives in `src/`, and unit
tests are in `tests/`.

### Installation

```bash
git clone <repo-url>
cd cs6840finalProject
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

Execute the test suite from the repository root:

```bash
pytest
```

## C Implementation

A standalone C11 port of the explicit CTL model checker lives in `c_src/`.
Build the CLI binary with `make` and provide a text file describing the
transition system and formula:

```bash
make -C c_src
./c_src/ctl_checker path/to/input.txt
```

The input format is line-oriented:

```
states <num_states>
init <k> <s0> ... <sk-1>
transitions <m>
u0 v0
...
u(m-1) v(m-1)
labels <l>
state count label0 ... label(count-1)
...
<formula>
```

For example:

```
states 2
init 1 0
transitions 2
0 1
1 1
labels 2
0 1 q
1 1 p
EF p
```

The program prints `true` when all initial states satisfy the formula and
exits with a zero status code; otherwise it prints `false` and exits non-zero.

## Example Usage

A minimal demonstration is provided in `example_usage.py`:

```bash
python example_usage.py
```

The script prints a label and result for each CTL formula, e.g.:

```
BDD EF p: True
BDD AG p: False
...
Explicit A[q U p]: False
```

## Benchmarks

Two benchmarking scripts live in the `benchmarks/` directory:

- `run_benchmarks.py` compares runtime and peak memory usage of the BDD and
  explicit checkers on a ring topology.
- `variable_order.py` measures the effect of reversing the BDD variable order
  on a simple chain.

Run them from the repository root:

```bash
python benchmarks/run_benchmarks.py
python benchmarks/variable_order.py
```

Sample results are available in
[BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md).

## Documentation

For an overview of project goals, module layout, and example workflows, see
[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md).

<p align="right"><a href="#readme-top">back to top</a></p>

