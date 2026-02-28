import ast

from countdown.solver import solve_numbers


def safe_eval(expr: str) -> int:
    """Evaluate a simple arithmetic expression safely (no builtins, no names)."""

    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Only numeric constants allowed")
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            if isinstance(n.op, ast.Add):
                return left + right
            if isinstance(n.op, ast.Sub):
                return left - right
            if isinstance(n.op, ast.Mult):
                return left * right
            if isinstance(n.op, ast.Div):
                return left / right
            raise ValueError("Unsupported operator")
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            val = _eval(n.operand)
            return +val if isinstance(n.op, ast.UAdd) else -val
        raise ValueError("Unsupported expression")

    return _eval(node)


def test_solve_numbers_simple():
    expr = solve_numbers([1, 2, 3], 7)
    assert isinstance(expr, str)
    assert safe_eval(expr) == 7


def test_solve_numbers_none():
    assert solve_numbers([1, 1], 3) is None
