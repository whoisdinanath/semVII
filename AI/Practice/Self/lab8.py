# lab8.py

import itertools
import re

def extract_variables(expr):
    """
    Extract all unique variable names (A-Z) from the expression.
    """
    variables = set()
    for char in expr:
        if char.isalpha():
            variables.add(char)
    return sorted(variables)


def convert_symbols(expr):
    """
    Convert logical operators to Python equivalents:
        ¬ -> not
        ∧ -> and
        ∨ -> or
    Note: → and ↔ are handled separately.
    """
    expr = expr.replace("¬", " not ")
    expr = expr.replace("∧", " and ")
    expr = expr.replace("∨", " or ")
    return expr


def expand_implications(expr):
    """
    Replace all → and ↔ with equivalent Python logic expressions.
    This handles both atomic and nested subexpressions.

    A → B becomes (not A or B)
    A ↔ B becomes ((A and B) or (not A and not B))
    """
    # Replace ↔ with equivalence
    while '↔' in expr:
        expr = re.sub(r'\(([^()]+)\)\s*↔\s*\(([^()]+)\)', r'((\1 and \2) or (not \1 and not \2))', expr)
        expr = re.sub(r'([A-Z])\s*↔\s*\(([^()]+)\)', r'((\1 and \2) or (not \1 and not \2))', expr)
        expr = re.sub(r'\(([^()]+)\)\s*↔\s*([A-Z])', r'((\1 and \2) or (not \1 and not \2))', expr)
        expr = re.sub(r'([A-Z])\s*↔\s*([A-Z])', r'((\1 and \2) or (not \1 and not \2))', expr)

    # Replace → with implication
    while '→' in expr:
        expr = re.sub(r'\(([^()]+)\)\s*→\s*\(([^()]+)\)', r'(not (\1) or (\2))', expr)
        expr = re.sub(r'([A-Z])\s*→\s*\(([^()]+)\)', r'(not \1 or (\2))', expr)
        expr = re.sub(r'\(([^()]+)\)\s*→\s*([A-Z])', r'(not (\1) or \2)', expr)
        expr = re.sub(r'([A-Z])\s*→\s*([A-Z])', r'(not \1 or \2)', expr)

    return expr


def eval_expr(expr, value_map):
    """
    Replace variables in the expression with boolean values and evaluate it.
    """
    eval_expr = expr
    for var, val in value_map.items():
        eval_expr = eval_expr.replace(var, str(val))
    try:
        return eval(eval_expr)
    except Exception as e:
        print(f"Error evaluating expression: {eval_expr}")
        raise e


def truth_table(expr):
    """
    Construct and print a truth table for the logical expression.
    """
    print(f"\nExpression: {expr}")

    variables = extract_variables(expr)
    expr = convert_symbols(expr)
    expr = expand_implications(expr)

    combinations = list(itertools.product([False, True], repeat=len(variables)))

    # Header
    print("\n" + " | ".join(variables) + " | Result")
    print("-" * (len(variables) * 6 + 10))

    for combo in combinations:
        value_map = dict(zip(variables, combo))
        result = eval_expr(expr, value_map)
        row = " | ".join(str(int(value_map[v])) for v in variables)
        print(f"{row} |   {int(result)}")


def main():
    expressions = [
        "¬A ∨ B",
        "A ∧ B → C",
        "A ↔ B",
        "A ∨ ¬B ∧ C",
        "(A ∧ B) ↔ (C ∨ ¬A)"
    ]

    for expr in expressions:
        truth_table(expr)


if __name__ == "__main__":
    main()