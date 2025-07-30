"""Minimal example showing how to run the CTL model checker.

Run ``python example_usage.py`` from the repository root to execute the
snippet that appears in step 5 of the README.
"""

from src.bddctl import TransitionSystem, CTLModelChecker
from src.explicitctl import ExplicitTransitionSystem, ExplicitCTLModelChecker


def main() -> None:
    """Run a few CTL queries with both backends to demonstrate the model checker."""

    # BDD-based transition systems
    ts = TransitionSystem(
        num_states=2,
        transitions=[(0, 1), (1, 1)],
        labeling={0: {"q"}, 1: {"p"}},
        init={0},
    )

    ts_until = TransitionSystem(
        num_states=3,
        transitions=[
            (0, 1),
            (1, 1),
            (1, 2),
            (2, 2),
        ],
        labeling={0: {"q"}, 1: {"q"}, 2: {"p"}},
        init={0},
    )

    # Explicit transition systems
    ets = ExplicitTransitionSystem(
        num_states=2,
        transitions=[(0, 1), (1, 1)],
        labeling={0: {"q"}, 1: {"p"}},
        init={0},
    )

    ets_until = ExplicitTransitionSystem(
        num_states=3,
        transitions=[
            (0, 1),
            (1, 1),
            (1, 2),
            (2, 2),
        ],
        labeling={0: {"q"}, 1: {"q"}, 2: {"p"}},
        init={0},
    )

    bdd_mc = CTLModelChecker(ts)
    bdd_mc_until = CTLModelChecker(ts_until)
    explicit_mc = ExplicitCTLModelChecker(ets)
    explicit_mc_until = ExplicitCTLModelChecker(ets_until)

    queries = [
        ("BDD EF p", bdd_mc.satisfies("EF p")),
        ("BDD AG p", bdd_mc.satisfies("AG p")),
        ("BDD AF p", bdd_mc.satisfies("AF p")),
        ("BDD EG q", bdd_mc.satisfies("EG q")),
        ("BDD E[q U p]", bdd_mc_until.satisfies("E[q U p]")),
        ("BDD A[q U p]", bdd_mc_until.satisfies("A[q U p]")),
        ("Explicit EF p", explicit_mc.satisfies("EF p")),
        ("Explicit AG p", explicit_mc.satisfies("AG p")),
        ("Explicit AF p", explicit_mc.satisfies("AF p")),
        ("Explicit EG q", explicit_mc.satisfies("EG q")),
        ("Explicit E[q U p]", explicit_mc_until.satisfies("E[q U p]")),
        ("Explicit A[q U p]", explicit_mc_until.satisfies("A[q U p]")),
    ]

    print("Results of example CTL queries:")
    for label, result in queries:
        print(f"{label}: {result}")


if __name__ == "__main__":
    main()
