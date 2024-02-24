from string import capwords
from functools import reduce
from collections import defaultdict


def calculate_lengths(name: str, fields: list[dict]):
    column_lengths = defaultdict(lambda: 0)
    for field in fields:
        for key, value in field.items():
            value = value or '-'
            column_lengths[key] = max(column_lengths[key], len(value), len(key))
    return column_lengths 

def format_value(value, length):
    value = value or '-'
    padding = length - len(value)
    return value + (padding * " ")

def format_table(name: str, fields: list[dict]):
    column_lengths = calculate_lengths(name, fields)
    print(name)
    line = []
    for key, length in column_lengths.items():
        line.append(format_value(key, length))
    print(" ".join(line))
    for field in fields:
        line = []
        for key, value in field.items():
            line.append(format_value(value, column_lengths[key]))
        print(" ".join(line))
    print("\n")