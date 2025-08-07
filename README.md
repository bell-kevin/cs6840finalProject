<a name="readme-top"></a>

# BDD-Based CTL Model Checker

A Python implementation of a Computation Tree Logic (CTL) model checker that
represents state sets symbolically using Binary Decision Diagrams (BDDs). A
reference explicit-state checker is included for comparison and benchmarking.

## Table of Contents
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Example Usage](#example-usage)
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

