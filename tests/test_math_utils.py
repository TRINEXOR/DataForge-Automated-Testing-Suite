"""
test_math_utils.py
Unit tests for dataforge.MathUtils
"""

import pytest
from dataforge.math_utils import MathUtils


# ──────────────────────────────────────────────────────────────
# factorial()
# ──────────────────────────────────────────────────────────────
class TestFactorial:
    def test_zero(self):
        assert MathUtils.factorial(0) == 1

    def test_one(self):
        assert MathUtils.factorial(1) == 1

    def test_small(self):
        assert MathUtils.factorial(5) == 120

    def test_large(self):
        assert MathUtils.factorial(10) == 3628800

    def test_negative(self):
        with pytest.raises(ValueError):
            MathUtils.factorial(-1)

    def test_float_input(self):
        with pytest.raises(TypeError):
            MathUtils.factorial(3.0)

    def test_string_input(self):
        with pytest.raises(TypeError):
            MathUtils.factorial("5")


# ──────────────────────────────────────────────────────────────
# is_prime()
# ──────────────────────────────────────────────────────────────
class TestIsPrime:
    def test_two_is_prime(self):
        assert MathUtils.is_prime(2) is True

    def test_three_is_prime(self):
        assert MathUtils.is_prime(3) is True

    def test_four_not_prime(self):
        assert MathUtils.is_prime(4) is False

    def test_one_not_prime(self):
        assert MathUtils.is_prime(1) is False

    def test_zero_not_prime(self):
        assert MathUtils.is_prime(0) is False

    def test_negative_not_prime(self):
        assert MathUtils.is_prime(-7) is False

    def test_large_prime(self):
        assert MathUtils.is_prime(97) is True

    def test_large_composite(self):
        assert MathUtils.is_prime(100) is False

    def test_known_primes(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for p in primes:
            assert MathUtils.is_prime(p) is True, f"{p} should be prime"

    def test_type_error(self):
        with pytest.raises(TypeError):
            MathUtils.is_prime(3.5)


# ──────────────────────────────────────────────────────────────
# gcd()
# ──────────────────────────────────────────────────────────────
class TestGcd:
    def test_basic(self):
        assert MathUtils.gcd(12, 8) == 4

    def test_coprime(self):
        assert MathUtils.gcd(7, 13) == 1

    def test_same_numbers(self):
        assert MathUtils.gcd(9, 9) == 9

    def test_one_zero(self):
        assert MathUtils.gcd(0, 5) == 5

    def test_both_zero(self):
        assert MathUtils.gcd(0, 0) == 0

    def test_negative_inputs(self):
        assert MathUtils.gcd(-12, 8) == 4

    def test_large_numbers(self):
        assert MathUtils.gcd(1000000, 500000) == 500000

    def test_type_error(self):
        with pytest.raises(TypeError):
            MathUtils.gcd(1.5, 3)


# ──────────────────────────────────────────────────────────────
# lcm()
# ──────────────────────────────────────────────────────────────
class TestLcm:
    def test_basic(self):
        assert MathUtils.lcm(4, 6) == 12

    def test_coprime(self):
        assert MathUtils.lcm(5, 7) == 35

    def test_one_is_zero(self):
        assert MathUtils.lcm(0, 5) == 0

    def test_same_numbers(self):
        assert MathUtils.lcm(9, 9) == 9

    def test_type_error(self):
        with pytest.raises(TypeError):
            MathUtils.lcm(2.0, 3)


# ──────────────────────────────────────────────────────────────
# mean()
# ──────────────────────────────────────────────────────────────
class TestMean:
    def test_integers(self):
        assert MathUtils.mean([1, 2, 3, 4, 5]) == 3.0

    def test_floats(self):
        assert abs(MathUtils.mean([1.5, 2.5]) - 2.0) < 1e-9

    def test_single_element(self):
        assert MathUtils.mean([42]) == 42.0

    def test_negatives(self):
        assert MathUtils.mean([-1, 0, 1]) == 0.0

    def test_empty_list(self):
        with pytest.raises(ValueError):
            MathUtils.mean([])

    def test_not_a_list(self):
        with pytest.raises(TypeError):
            MathUtils.mean(5)

    def test_non_numeric_element(self):
        with pytest.raises(TypeError):
            MathUtils.mean([1, "two", 3])


# ──────────────────────────────────────────────────────────────
# median()
# ──────────────────────────────────────────────────────────────
class TestMedian:
    def test_odd_count(self):
        assert MathUtils.median([3, 1, 2]) == 2.0

    def test_even_count(self):
        assert MathUtils.median([1, 2, 3, 4]) == 2.5

    def test_single_element(self):
        assert MathUtils.median([7]) == 7.0

    def test_unsorted_input(self):
        assert MathUtils.median([5, 1, 3]) == 3.0

    def test_empty_list(self):
        with pytest.raises(ValueError):
            MathUtils.median([])

    def test_non_numeric(self):
        with pytest.raises(TypeError):
            MathUtils.median([1, "x"])

    def test_type_error(self):
        with pytest.raises(TypeError):
            MathUtils.median("1,2,3")


# ──────────────────────────────────────────────────────────────
# fibonacci()
# ──────────────────────────────────────────────────────────────
class TestFibonacci:
    def test_zero_terms(self):
        assert MathUtils.fibonacci(0) == []

    def test_one_term(self):
        assert MathUtils.fibonacci(1) == [0]

    def test_two_terms(self):
        assert MathUtils.fibonacci(2) == [0, 1]

    def test_ten_terms(self):
        assert MathUtils.fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_negative(self):
        with pytest.raises(ValueError):
            MathUtils.fibonacci(-1)

    def test_type_error(self):
        with pytest.raises(TypeError):
            MathUtils.fibonacci(5.0)

    def test_sequence_property(self):
        """Each element (after first two) equals sum of previous two."""
        seq = MathUtils.fibonacci(15)
        for i in range(2, len(seq)):
            assert seq[i] == seq[i - 1] + seq[i - 2]


# ──────────────────────────────────────────────────────────────
# clamp()
# ──────────────────────────────────────────────────────────────
class TestClamp:
    def test_within_range(self):
        assert MathUtils.clamp(5, 0, 10) == 5

    def test_below_min(self):
        assert MathUtils.clamp(-5, 0, 10) == 0

    def test_above_max(self):
        assert MathUtils.clamp(15, 0, 10) == 10

    def test_at_min(self):
        assert MathUtils.clamp(0, 0, 10) == 0

    def test_at_max(self):
        assert MathUtils.clamp(10, 0, 10) == 10

    def test_floats(self):
        assert MathUtils.clamp(1.5, 1.0, 2.0) == 1.5

    def test_invalid_range(self):
        with pytest.raises(ValueError):
            MathUtils.clamp(5, 10, 0)
