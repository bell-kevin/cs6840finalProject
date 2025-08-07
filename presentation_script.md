# Presentation Script: Developing a BDD-Based CTL Model Checker

> **Audience**: Dr. Rague  
> **Format**: 15‑minute recorded presentation

---
## Slide 1 – Title (0:00–0:30)
*Hello and welcome.* My name is Kevin Bell, and this is my final project for CS 6840, Formal System Design. In the next fifteen minutes I’ll walk through the motivation, design, and results of my BDD‑based CTL model checker.

---
## Slide 2 – Motivation (0:30–1:45)
Computational Tree Logic, or CTL, allows us to express properties about all possible execution paths of a system. Traditional explicit-state model checkers explore every reachable state, but that can explode exponentially. Binary Decision Diagrams, or BDDs, let us encode sets of states compactly, so symbolic algorithms can scale further. This project explores that contrast by building both symbolic and explicit checkers.

---
## Slide 3 – Project Goals (1:45–2:45)
The primary goals are threefold: implement a CTL checker using the `dd` BDD library, provide an explicit-state baseline that shares the same interface, and gather performance data to see how BDD variable ordering affects efficiency.

---
## Slide 4 – CTL & Operators (2:45–4:00)
Before diving into code, a quick refresher. CTL formulas combine propositional logic with temporal operators. For example, `EF p` means “there exists a path where eventually `p` holds,” and `AG p` means “on all paths, `p` holds globally.” Most of these operators have fixpoint characterizations, so evaluating a formula becomes an iterative process until a set of states stabilizes.

---
## Slide 5 – Transition System Representation (4:00–5:30)
The `TransitionSystem` class constructs BDD variables for the bits representing current and next states. Transitions are encoded as a single BDD relation. Labeling maps each state to its true propositions. This structure allows efficient predecessor and successor computations via relational products.

---
## Slide 6 – Symbolic Model Checker (5:30–7:00)
`CTLModelChecker` parses a formula into an abstract syntax tree, then recursively evaluates it. Boolean connectives map to BDD operations, `EX` uses the predecessor function, and operators like `EF` or `EG` rely on least or greatest fixpoints implemented with simple loops. The end result is a BDD representing all states that satisfy the formula.

---
## Slide 7 – Explicit Model Checker (7:00–8:15)
For validation and comparison, `ExplicitTransitionSystem` stores successor sets explicitly. `ExplicitCTLModelChecker` implements the same algorithms using Python sets instead of BDDs. Both backends expose a `satisfies` method so tests and examples can run them interchangeably.

---
## Slide 8 – Example Usage (8:15–9:30)
The repository includes a small script, `example_usage.py`, that builds tiny transition systems and runs a collection of CTL formulas against both checkers. The output confirms they agree on all results, serving as a quick sanity check.

---
## Slide 9 – Benchmarks (9:30–10:45)
Two benchmarking scripts explore performance. `run_benchmarks.py` compares runtime and peak memory for ring topologies as the number of states grows. `variable_order.py` demonstrates how simply reversing the BDD variable order can increase BDD sizes and slow the model checker, underscoring the importance of good ordering.

---
## Slide 10 – Testing & Verification (10:45–12:00)
A suite of sixteen unit tests exercises all major CTL operators. Each test builds a small system and checks that both the BDD and explicit implementations produce the expected truth value. Continuous testing ensured refactors didn’t introduce regressions.

---
## Slide 11 – Lessons Learned (12:00–13:00)
Three key takeaways: first, BDD variable ordering has a dramatic effect on memory usage. Second, symbolic methods shine when the state space is large but has regular structure. Third, Python’s `dd` library and Lark parser make it straightforward to prototype complex algorithms.

---
## Slide 12 – Future Work (13:00–14:00)
Given more time, I’d like to add support for fairness constraints, explore dynamic variable reordering, and scale the benchmarks to larger, possibly real‑world systems.

---
## Slide 13 – Conclusion (14:00–15:00)
To wrap up, this project delivers a minimal yet complete CTL model checker with both symbolic and explicit backends. The code, tests, and benchmarks are all available in the repository. Thank you for watching, and I hope this tool provides a solid foundation for further exploration in formal system design.
