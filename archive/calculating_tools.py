
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds a and b and returns the result as a number. The response is always correct."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b and returns the result as a number. The response is always correct."""
    return a * b

@tool
def times_two(a: int) -> int:
    """Accepts a number and returns twice that number. The response is always correct."""
    return a * 2

