from src.bddctl import TransitionSystem, CTLModelChecker

# Simple example demonstrating how to use the CTL model checker

ts = TransitionSystem(
    num_states=2,
    transitions=[(0, 1), (1, 1)],
    labeling={0: {"q"}, 1: {"p"}},
    init={0},
)

mc = CTLModelChecker(ts)
print(mc.satisfies("EF p"))
