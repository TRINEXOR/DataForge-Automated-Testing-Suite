"""
math_utils.py - Mathematical operation utilities for DataForge.
"""

from typing import List, Union
import math

Number = Union[int, float]


class MathUtils:
    """A collection of mathematical utilities."""

    @staticmethod
    def factorial(n: int) -> int:
        """
        Compute the factorial of a non-negative integer.

        Args:
            n: Non-negative integer.

        Returns:
            n!
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected int, got {type(n).__name__}")
        if n < 0:
            raise ValueError("Factorial is not defined for negative integers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Determine whether n is a prime number.

        Args:
            n: Integer to check.

        Returns:
            True if n is prime, False otherwise.
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected int, got {type(n).__name__}")
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.isqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Return the Greatest Common Divisor of two integers."""
        if not (isinstance(a, int) and isinstance(b, int)):
            raise TypeError("Both arguments must be integers")
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Return the Least Common Multiple of two integers."""
        if not (isinstance(a, int) and isinstance(b, int)):
            raise TypeError("Both arguments must be integers")
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // MathUtils.gcd(a, b)

    @staticmethod
    def mean(numbers: List[Number]) -> float:
        """Compute the arithmetic mean of a list of numbers."""
        if not isinstance(numbers, list):
            raise TypeError("Expected a list")
        if len(numbers) == 0:
            raise ValueError("Cannot compute mean of an empty list")
        for n in numbers:
            if not isinstance(n, (int, float)):
                raise TypeError(f"All elements must be numeric, got {type(n).__name__}")
        return sum(numbers) / len(numbers)

    @staticmethod
    def median(numbers: List[Number]) -> float:
        """Compute the median of a list of numbers."""
        if not isinstance(numbers, list):
            raise TypeError("Expected a list")
        if len(numbers) == 0:
            raise ValueError("Cannot compute median of an empty list")
        for n in numbers:
            if not isinstance(n, (int, float)):
                raise TypeError(f"All elements must be numeric, got {type(n).__name__}")
        sorted_nums = sorted(numbers)
        mid = len(sorted_nums) // 2
        if len(sorted_nums) % 2 == 1:
            return float(sorted_nums[mid])
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2.0

    @staticmethod
    def fibonacci(n: int) -> List[int]:
        """
        Generate the first n Fibonacci numbers.

        Args:
            n: Number of terms (must be >= 0).

        Returns:
            List of Fibonacci numbers.
        """
        if not isinstance(n, int):
            raise TypeError(f"Expected int, got {type(n).__name__}")
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return []
        if n == 1:
            return [0]
        seq = [0, 1]
        for _ in range(2, n):
            seq.append(seq[-1] + seq[-2])
        return seq

    @staticmethod
    def clamp(value: Number, min_val: Number, max_val: Number) -> Number:
        """Clamp a value between min_val and max_val."""
        if min_val > max_val:
            raise ValueError("min_val must be <= max_val")
        return max(min_val, min(value, max_val))
