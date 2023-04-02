import ast
import unittest

# Optimization (constant folding) of AST

def optimize(node):
    return node

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
