import ast
import json
import subprocess
import sys


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "countdown", *args],
        capture_output=True,
        text=True,
    )


def _safe_eval_expr(expr: str) -> int:
    """Safely evaluate an arithmetic expression consisting of +,-,*,/ and parentheses.

    Uses AST validation and performs integer division for '/'.
    """

    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, int):
                raise ValueError("Only integer constants are allowed")
            return int(node.value)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            v = eval_node(node.operand)
            return v if isinstance(node.op, ast.UAdd) else -v

        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left = eval_node(node.left)
            right = eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError
                # Countdown solver uses exact divisibility; treat '/' as integer division.
                if left % right != 0:
                    raise ValueError("Non-integer division")
                return left // right

        raise ValueError(f"Disallowed expression node: {type(node).__name__}")

    tree = ast.parse(expr, mode="eval")

    # Ensure there are no names, calls, attributes, subscripts, etc.
    for n in ast.walk(tree):
        if isinstance(
            n,
            (
                ast.Name,
                ast.Call,
                ast.Attribute,
                ast.Subscript,
                ast.Lambda,
                ast.Dict,
                ast.List,
                ast.Tuple,
                ast.Set,
                ast.ListComp,
                ast.SetComp,
                ast.DictComp,
                ast.GeneratorExp,
                ast.Await,
                ast.Yield,
                ast.YieldFrom,
                ast.Compare,
                ast.BoolOp,
                ast.IfExp,
                ast.JoinedStr,
                ast.FormattedValue,
            ),
        ):
            raise ValueError(f"Disallowed expression construct: {type(n).__name__}")

    return int(eval_node(tree))


def test_cli_generate():
    proc = _run_cli(
        "generate",
        "--count",
        "3",
        "--min",
        "1",
        "--max",
        "3",
        "--target-min",
        "10",
        "--target-max",
        "20",
        "--seed",
        "0",
    )
    assert proc.returncode == 0, proc.stderr

    payload = json.loads(proc.stdout)
    assert set(payload.keys()) >= {"numbers", "target"}

    numbers = payload["numbers"]
    target = payload["target"]

    assert isinstance(numbers, list)
    assert len(numbers) == 3
    assert all(isinstance(n, int) for n in numbers)
    assert all(1 <= n <= 3 for n in numbers)

    assert isinstance(target, int)
    assert 10 <= target <= 20


def test_cli_solve():
    proc = _run_cli("solve", "--numbers", "1,2,3", "--target", "7")
    assert proc.returncode == 0, proc.stderr

    out = proc.stdout.strip()
    assert out != "NO_SOLUTION"

    value = _safe_eval_expr(out)
    assert value == 7
