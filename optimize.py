from operator import add, sub, mul
import ast
import unittest

# Optimization (constant folding) of AST

def optimize(node):
    if isinstance(node, ast.Constant):
        return node
    elif isinstance(node, ast.Name):
        return node
    elif isinstance(node, ast.Expression):
        return optimize(node.body)
    elif isinstance(node, ast.BinOp):
        a = optimize(node.left)
        b = optimize(node.right)
        # No need to do constant folding if either left or right is not a constant
        if (not isinstance(a, ast.Constant) or not isinstance(b, ast.Constant)):
            node.left = a
            node.right = b
            return node
        foldConstant = { ast.Add: add, ast.Sub: sub, ast.Mult: mul }.get(type(node.op))(a.value, b.value)
        return ast.Constant(foldConstant)

class TestOptimize(unittest.TestCase):
    def test_optimize(self):
        test_cases = [
            ('x + (1 + 2)', 'x + 3'),
            ('1 + 2 * 3', '7'),
            ('x + 1', 'x + 1'),
            ('(2 + 3) * x + y * (z + (2 - 1) * 3)', '5 * x + y * (z + 3)'),
        ]
        for s, expected in test_cases:
            expr = ast.parse(s, mode='eval')
            # Uncomment to print AST for expression
            # print(ast.dump(expr, indent=2))
            optimized = optimize(expr)
            # print(ast.dump(optimized, indent=2))
            actual = ast.unparse(optimized)
            if actual != expected:
                raise AssertionError(f'"{s}": expected "{expected}", got "{actual}"')

if __name__ == '__main__':
    unittest.main()
