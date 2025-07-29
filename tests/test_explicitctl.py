import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.explicitctl import ExplicitTransitionSystem, ExplicitCTLModelChecker


def build_ts():
    transitions = [(0, 1), (1, 1)]
    labeling = {
        0: {"q"},
        1: {"p"}
    }
    ts = ExplicitTransitionSystem(num_states=2, transitions=transitions, labeling=labeling, init={0})
    return ts


def build_ts_until():
    """Three-state system for testing until formulas."""
    transitions = [
        (0, 1),
        (1, 1),
        (1, 2),
        (2, 2),
    ]
    labeling = {
        0: {"q"},
        1: {"q"},
        2: {"p"},
    }
    return ExplicitTransitionSystem(num_states=3, transitions=transitions, labeling=labeling, init={0})


def test_ef_p():
    ts = build_ts()
    mc = ExplicitCTLModelChecker(ts)
    assert mc.satisfies("EF p")


def test_ag_p_false():
    ts = build_ts()
    mc = ExplicitCTLModelChecker(ts)
    assert not mc.satisfies("AG p")


def test_af_p_true():
    ts = build_ts()
    mc = ExplicitCTLModelChecker(ts)
    assert mc.satisfies("AF p")


def test_eg_q_false():
    ts = build_ts()
    mc = ExplicitCTLModelChecker(ts)
    assert not mc.satisfies("EG q")


def test_eu_q_until_p_true():
    ts = build_ts_until()
    mc = ExplicitCTLModelChecker(ts)
    assert mc.satisfies("E[q U p]")


def test_au_q_until_p_false():
    ts = build_ts_until()
    mc = ExplicitCTLModelChecker(ts)
    assert not mc.satisfies("A[q U p]")
