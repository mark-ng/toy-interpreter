from collections import defaultdict
from operator import add, sub, mul
import ast
import unittest
from optimize import optimize

# Generate fictional assembly by tree-walking an AST

X_REGISTER = 'r1'
Y_REGISTER = 'r2'

def codegen(expr):
    registerMapping = { 'x': X_REGISTER, 'y': Y_REGISTER}
    if isinstance(expr, ast.Name):
        return [f"MOV %{registerMapping[expr.id]} %r0"]
    elif isinstance(expr, ast.Constant):
        return [f"MOV ${expr.value} %r0"]
    elif isinstance(expr, ast.BinOp):
        leftASM = codegen(expr.left)
        rightASM = codegen(expr.right)
        # Check if register already used in nested recursion
        pickedRegisterNum = 3
        while True:
            if f"%r{pickedRegisterNum}" not in " ".join(leftASM + rightASM): break
            pickedRegisterNum += 1
        op_map = { ast.Add: "ADD", ast.Sub: "SUB", ast.Mult: "MUL"}
        op_code = op_map[type(expr.op)]
        return [*leftASM, f"MOV %r0 %r{pickedRegisterNum}", *rightASM, f"{op_code} %r{pickedRegisterNum} %r0 %r0"]
    # When expr is ast.Expression
    return codegen(expr.body)

OP_TO_FUNCTION = {
    'ADD': add,
    'SUB': sub,
    'MUL': mul,
}

def run_assembly_program(instructions, x, y):
    registers = defaultdict(int)
    registers[X_REGISTER] = x
    registers[Y_REGISTER] = y
    def input_operand(arg):
        if arg[0] == '$':
            return int(arg[1:])
        elif arg[0] == '%':
            if arg[1] != 'r' or not arg[2:].isdigit():
                raise ValueError(f'invalid register {arg}')
            return registers[arg[1:]]
        else:
            raise ValueError(f'invalid input operand {arg}')
    def output_operand(arg):
        if arg[0] != '%':
            raise ValueError(f'invalid output operand {arg}')
        return arg[1:]
    for instruction in instructions:
        parts = instruction.strip().split()
        if parts[0] == 'MOV':
            in1 = input_operand(parts[1])
            out1 = output_operand(parts[2])
            registers[out1] = in1
        elif parts[0] in OP_TO_FUNCTION:
            f = OP_TO_FUNCTION[parts[0]]
            in1 = input_operand(parts[1])
            in2 = input_operand(parts[2])
            out1 = output_operand(parts[3])
            registers[out1] = f(in1, in2)
        else:
            raise ValueError(f'invalid instruction {instruction}')
    return registers['r0']

class TestCodegen(unittest.TestCase):
    def test_codegen(self):
        # For each test case, generate assembly, then run it to make sure
        # it produces the expected answer.
        test_cases = [
            ('1 + 1', (0, 0), 2),
            ('1 + 2 * 3', (0, 0), 7),
            ('1 + 2 * (3 - 4)', (0, 0), -1),
            ('1 + (2 - 3) * 4 + 5', (0, 0), 2),
            ('x', (5, 4), 5),
            ('x + 1', (10, 0), 11),
            ('y + 1', (10, 0), 1),
            ('x + y + 1', (1, 2), 4),
            ('2 * ((x - 1) * (y + 2)) + x', (3, 5), 31),
            ('1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + x + y', (9, 10), 55), 
        ]
        for s, (x, y), expected in test_cases:
            expr = ast.parse(s, mode='eval')
            # Uncomment to turn on AST optimization
            # expr = optimize(expr)
            # Uncomment to print AST for expression
            print(ast.dump(expr, indent=2))
            program = codegen(expr)
            # Uncomment to print result of codegen
            print(program)
            actual = run_assembly_program(program, x, y)
            if actual != expected:
                raise AssertionError(f'"{s}": expected "{expected}", got "{actual}"')

if __name__ == '__main__':
    unittest.main()
