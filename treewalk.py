from operator import add, sub, mul
import ast
import unittest

# Tree-Walk evaluation stimulation of AST from Python's `ast` module

def evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Expression):
        return evaluate(node.body)
    elif isinstance(node, ast.BinOp):
        a = evaluate(node.left)
        b = evaluate(node.right)
        return { ast.Add: add, ast.Sub: sub, ast.Mult: mul }.get(type(node.op))(a, b)

class TestEvaluate(unittest.TestCase):
    def test_evaluate(self):
        test_cases = [
            ('1 + 1', 2),
            ('1 + 2 * 3', 7),
            ('1 + 2 * (3 - 4)', -1),
            ('1 + (2 - 3) * 4 + 5', 2),
        ]
        for s, expected in test_cases:
            expr = ast.parse(s, mode='eval')
            # Uncomment to print AST for expression
            print(ast.dump(expr, indent=2))
            actual = evaluate(expr)
            if actual != expected:
                raise AssertionError(f'"{s}": expected {expected}, got {actual}')

if __name__ == '__main__':
    unittest.main()