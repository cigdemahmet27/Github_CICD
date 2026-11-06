"""Simple math functions. The pipeline lints and tests this code."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("average() needs at least one number")
    return sum(numbers) / len(numbers)
