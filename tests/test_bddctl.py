import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.bddctl import TransitionSystem, CTLModelChecker


def build_ts():
    transitions = [(0, 1), (1, 1)]
    labeling = {
        0: {"q"},
        1: {"p"}
    }
    ts = TransitionSystem(num_states=2, transitions=transitions, labeling=labeling, init={0})
    return ts


def test_ef_p():
    ts = build_ts()
    mc = CTLModelChecker(ts)
    assert mc.satisfies("EF p")


def test_ag_p_false():
    ts = build_ts()
    mc = CTLModelChecker(ts)
    assert not mc.satisfies("AG p")


def test_af_p_true():
    ts = build_ts()
    mc = CTLModelChecker(ts)
    assert mc.satisfies("AF p")


def test_eg_q_false():
    ts = build_ts()
    mc = CTLModelChecker(ts)
    assert not mc.satisfies("EG q")
