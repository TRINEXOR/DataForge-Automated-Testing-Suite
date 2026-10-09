"""
string_utils.py - String manipulation utilities for DataForge.
"""

import re
from typing import List, Optional


class StringUtils:
    """A collection of string manipulation utilities."""

    @staticmethod
    def reverse(text: str) -> str:
        """Return the reversed version of a string."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        return text[::-1]

    @staticmethod
    def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
        """
        Check whether a string is a palindrome.

        Args:
            text: The input string.
            ignore_case: If True, comparison is case-insensitive.
            ignore_spaces: If True, spaces are stripped before comparison.

        Returns:
            True if palindrome, False otherwise.
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")

        processed = text
        if ignore_spaces:
            processed = processed.replace(" ", "")
        if ignore_case:
            processed = processed.lower()

        return processed == processed[::-1]

    @staticmethod
    def word_count(text: str) -> int:
        """Return the number of words in a string."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        return len(text.split()) if text.strip() else 0

    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate a string to a maximum length, appending a suffix if truncated.

        Args:
            text: The input string.
            max_length: Maximum allowed length (including suffix).
            suffix: String appended when truncation occurs.

        Returns:
            Truncated (or original) string.
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        if max_length < 0:
            raise ValueError("max_length must be non-negative")
        if len(text) <= max_length:
            return text
        cut = max_length - len(suffix)
        if cut < 0:
            return suffix[:max_length]
        return text[:cut] + suffix

    @staticmethod
    def caesar_cipher(text: str, shift: int) -> str:
        """
        Apply a Caesar cipher shift to alphabetic characters.

        Args:
            text: Input string.
            shift: Number of positions to shift (can be negative).

        Returns:
            Encrypted/decrypted string.
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        if not isinstance(shift, int):
            raise TypeError("shift must be an integer")

        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """Extract all email addresses found in a string."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)

    @staticmethod
    def to_snake_case(text: str) -> str:
        """Convert a CamelCase or space-separated string to snake_case."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        # Insert underscore before uppercase letters that follow lowercase
        s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
        # Replace spaces/hyphens with underscore and lowercase everything
        return re.sub(r'[\s\-]+', '_', s1).lower()

    @staticmethod
    def count_vowels(text: str) -> int:
        """Count the number of vowels (a, e, i, o, u) in a string."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        return sum(1 for ch in text.lower() if ch in "aeiou")
