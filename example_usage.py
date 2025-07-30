"""Minimal example showing how to run the CTL model checker.

Run ``python example_usage.py`` from the repository root to execute the
snippet that appears in step 5 of the README.
"""

from src.bddctl import TransitionSystem, CTLModelChecker


def main() -> None:
    """Run a few CTL queries to demonstrate the model checker."""

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

    mc = CTLModelChecker(ts)
    mc_until = CTLModelChecker(ts_until)

    queries = [
        ("EF p", mc.satisfies("EF p")),
        ("AG p", mc.satisfies("AG p")),
        ("AF p", mc.satisfies("AF p")),
        ("EG q", mc.satisfies("EG q")),
        ("E[q U p]", mc_until.satisfies("E[q U p]")),
        ("A[q U p]", mc_until.satisfies("A[q U p]")),
    ]

    print("Results of example CTL queries:")
    for formula, result in queries:
        print(f"{formula}: {result}")


if __name__ == "__main__":
    main()