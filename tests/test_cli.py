import json
import subprocess
import sys


def _run(*args):
    return subprocess.run(
        [sys.executable, "-m", "countdown", *args],
        capture_output=True,
        text=True,
    )


def test_cli_generate_json():
    p = _run("generate", "--seed", "123")
    assert p.returncode == 0, p.stderr
    data = json.loads(p.stdout)
    assert set(data.keys()) == {"numbers", "target"}
    assert isinstance(data["numbers"], list)
    assert len(data["numbers"]) == 6
    assert all(isinstance(n, int) for n in data["numbers"])
    assert isinstance(data["target"], int)


def test_cli_solve_json():
    # Trivially solvable: 1+2=3
    p = _run("solve", "--numbers", "1,2", "--target", "3")
    assert p.returncode == 0, p.stderr
    data = json.loads(p.stdout)
    assert data["numbers"] == [1, 2]
    assert data["target"] == 3
    assert "solutions" in data
    assert isinstance(data["solutions"], list)
    assert len(data["solutions"]) >= 1
    assert any(expr in ("(1+2)", "(2+1)") for expr in data["solutions"])


def test_cli_solve_max_solutions_respected():
    p = _run("solve", "--numbers", "1,2", "--target", "3", "--max-solutions", "1")
    assert p.returncode == 0, p.stderr
    data = json.loads(p.stdout)
    assert len(data["solutions"]) <= 1
