# Developing a BDD-Based CTL Model Checker
Kevin Bell · CS 6840 Formal System Design · Summer 2025

---
## Motivation
- CTL model checking explores if a transition system satisfies temporal logic formulas
- Explicit enumeration suffers from state-space explosion
- Binary Decision Diagrams (BDDs) compactly encode large state sets

---
## Project Goals
- Implement a symbolic CTL checker using BDDs
- Provide an explicit-state baseline for comparison
- Analyze performance and variable-ordering effects

---
## CTL & Operators
- Propositional logic over paths and states
- Temporal operators: EX, AX, EF, AF, EG, AG, EU, AU
- Fixpoint characterizations enable iterative algorithms

---
## Transition System Representation
- `TransitionSystem` builds BDD variables for current and next state bits
- Transition relation stored as a single BDD
- Labeling maps states to atomic propositions

---
## Symbolic Model Checker
- `CTLModelChecker` evaluates formulas by recursive descent
- Predecessor computation via relational product
- Fixpoint routines for least and greatest fixpoints

---
## Explicit Model Checker
- `ExplicitTransitionSystem` keeps adjacency sets
- `ExplicitCTLModelChecker` mirrors symbolic interface using Python sets
- Useful for validation and performance comparison

---
## Example Usage
- Sample script runs both backends on tiny systems
- Demonstrates matching truth values for each CTL formula
- Serves as a sanity check and reference

---
## Benchmarks
- `run_benchmarks.py` compares runtime and memory on ring topologies
- `variable_order.py` highlights impact of BDD variable ordering
- Results summarized in `BENCHMARK_RESULTS.md`

---
## Testing & Verification
- 16 unit tests covering all major CTL operators
- Ensures parity between BDD and explicit implementations
- Automated via `pytest`

---
## Lessons Learned
- Variable ordering strongly influences BDD size
- Symbolic methods excel when states blow up but structure is regular
- Parsing and fixpoint algorithms compose cleanly in Python

---
## Future Work
- Support for fairness constraints and additional logics
- Incorporate dynamic variable reordering strategies
- Explore scalability on larger industrial benchmarks

---
## Conclusion
- Delivered a minimal yet complete CTL model checker
- Demonstrated symbolic vs. explicit trade-offs
- Code, tests, and benchmarks available in repository
