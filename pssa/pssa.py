"""
Singular Spectrum Analysis
=========================================================
The core module of the project
"""


def fib(n: int) -> int:
    """Fibonacci Number Generator.

    This will give you the n'th number in the Fibonacci sequence

    Args:
        n: The number position in the Fibonacci sequence

    Returns:
        The n'th number of in the Fibonacci sequence
    """
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def fib_ratio(n):
    """Fibonacci Ratio Generator.

    This will give you the n'th ratio in the Fibonacci sequence

    Args:
        n (int): The number position in the Fibonacci sequence
    Returns:
        float: The ratio of the n'th number of in the Fibonacci sequence
    """
    if n < 2:
        return n
    else:
        return fib(n - 1) / fib(n)


class MyClass(object):
    """This is a whole new class!

    This Singular Spectrum Analysis class is making classes great again.

    Args:
        name (str): The name of this class
    """

    def __init__(self, name: str):
        self.name = name
