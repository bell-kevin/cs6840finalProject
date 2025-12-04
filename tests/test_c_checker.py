import subprocess
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
BINARY_PATH = REPO_ROOT / "c_src" / "ctl_checker"


def generate_input(tmp_path, num_states, init_states, transitions, labels, formula):
    lines = [f"states {num_states}"]
    init_line = " ".join(str(s) for s in init_states)
    lines.append(f"init {len(init_states)} {init_line}")
    lines.append(f"transitions {len(transitions)}")
    for u, v in transitions:
        lines.append(f"{u} {v}")
    lines.append(f"labels {len(labels)}")
    for state, props in labels.items():
        props_line = " ".join(sorted(props))
        lines.append(f"{state} {len(props)} {props_line}")
    lines.append(formula)
    content = "\n".join(lines) + "\n"
    path = tmp_path / "input.txt"
    path.write_text(content)
    return path


@pytest.fixture(scope="session", autouse=True)
def build_c_binary():
    result = subprocess.run(["make", "-C", str(REPO_ROOT / "c_src")], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to build C binary: {result.stderr}")


def run_checker(input_path):
    completed = subprocess.run([str(BINARY_PATH), str(input_path)], capture_output=True, text=True)
    return completed.returncode, completed.stdout.strip()


def test_ef_p(tmp_path):
    transitions = [(0, 1), (1, 1)]
    labels = {0: {"q"}, 1: {"p"}}
    input_path = generate_input(tmp_path, 2, [0], transitions, labels, "EF p")
    code, output = run_checker(input_path)
    assert code == 0
    assert output == "true"


def test_ag_p_false(tmp_path):
    transitions = [(0, 1), (1, 1)]
    labels = {0: {"q"}, 1: {"p"}}
    input_path = generate_input(tmp_path, 2, [0], transitions, labels, "AG p")
    code, output = run_checker(input_path)
    assert code != 0
    assert output == "false"


def test_af_p_true(tmp_path):
    transitions = [(0, 1), (1, 1)]
    labels = {0: {"q"}, 1: {"p"}}
    input_path = generate_input(tmp_path, 2, [0], transitions, labels, "AF p")
    code, output = run_checker(input_path)
    assert code == 0
    assert output == "true"


def test_eg_q_false(tmp_path):
    transitions = [(0, 1), (1, 1)]
    labels = {0: {"q"}, 1: {"p"}}
    input_path = generate_input(tmp_path, 2, [0], transitions, labels, "EG q")
    code, output = run_checker(input_path)
    assert code != 0
    assert output == "false"


def test_eu_q_until_p_true(tmp_path):
    transitions = [(0, 1), (1, 1), (1, 2), (2, 2)]
    labels = {0: {"q"}, 1: {"q"}, 2: {"p"}}
    input_path = generate_input(tmp_path, 3, [0], transitions, labels, "E[q U p]")
    code, output = run_checker(input_path)
    assert code == 0
    assert output == "true"


def test_au_q_until_p_false(tmp_path):
    transitions = [(0, 1), (1, 1), (1, 2), (2, 2)]
    labels = {0: {"q"}, 1: {"q"}, 2: {"p"}}
    input_path = generate_input(tmp_path, 3, [0], transitions, labels, "A[q U p]")
    code, output = run_checker(input_path)
    assert code != 0
    assert output == "false"


def test_ex_p_true(tmp_path):
    transitions = [(0, 1), (1, 1)]
    labels = {0: {"q"}, 1: {"p"}}
    input_path = generate_input(tmp_path, 2, [0], transitions, labels, "EX p")
    code, output = run_checker(input_path)
    assert code == 0
    assert output == "true"


def test_ax_q_false(tmp_path):
    transitions = [(0, 1), (1, 1)]
    labels = {0: {"q"}, 1: {"p"}}
    input_path = generate_input(tmp_path, 2, [0], transitions, labels, "AX q")
    code, output = run_checker(input_path)
    assert code != 0
    assert output == "false"

