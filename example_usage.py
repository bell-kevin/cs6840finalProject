"""Minimal example showing how to run the CTL model checker.

Run ``python example_usage.py`` from the repository root to execute the
snippet that appears in step 5 of the README.
"""

from src.bddctl import TransitionSystem, CTLModelChecker


def main() -> None:
    """Instantiate a simple transition system and check a formula."""

    ts = TransitionSystem(
        num_states=2,
        transitions=[(0, 1), (1, 1)],
        labeling={0: {"q"}, 1: {"p"}},
        init={0},
    )

    mc = CTLModelChecker(ts)
    print(mc.satisfies("EF p"))


if __name__ == "__main__":
    main()
