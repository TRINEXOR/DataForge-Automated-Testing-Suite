"""
test_string_utils.py
Unit tests for dataforge.StringUtils
"""

import pytest
from dataforge.string_utils import StringUtils


# ──────────────────────────────────────────────────────────────
# reverse()
# ──────────────────────────────────────────────────────────────
class TestReverse:
    def test_regular_string(self):
        assert StringUtils.reverse("hello") == "olleh"

    def test_single_char(self):
        assert StringUtils.reverse("a") == "a"

    def test_empty_string(self):
        assert StringUtils.reverse("") == ""

    def test_palindrome_unchanged(self):
        assert StringUtils.reverse("racecar") == "racecar"

    def test_with_spaces(self):
        assert StringUtils.reverse("hello world") == "dlrow olleh"

    def test_numeric_string(self):
        assert StringUtils.reverse("12345") == "54321"

    def test_special_chars(self):
        assert StringUtils.reverse("!@#") == "#@!"

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.reverse(123)

    def test_type_error_none(self):
        with pytest.raises(TypeError):
            StringUtils.reverse(None)


# ──────────────────────────────────────────────────────────────
# is_palindrome()
# ──────────────────────────────────────────────────────────────
class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert StringUtils.is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert StringUtils.is_palindrome("hello") is False

    def test_case_insensitive(self):
        assert StringUtils.is_palindrome("RaceCar") is True

    def test_with_spaces(self):
        assert StringUtils.is_palindrome("a man a plan a canal panama") is True

    def test_single_char(self):
        assert StringUtils.is_palindrome("x") is True

    def test_empty_string(self):
        assert StringUtils.is_palindrome("") is True

    def test_case_sensitive_mode(self):
        assert StringUtils.is_palindrome("Racecar", ignore_case=False) is False

    def test_spaces_not_ignored(self):
        assert StringUtils.is_palindrome("race car", ignore_spaces=False) is False

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.is_palindrome(42)


# ──────────────────────────────────────────────────────────────
# word_count()
# ──────────────────────────────────────────────────────────────
class TestWordCount:
    def test_simple_sentence(self):
        assert StringUtils.word_count("Hello world") == 2

    def test_empty_string(self):
        assert StringUtils.word_count("") == 0

    def test_whitespace_only(self):
        assert StringUtils.word_count("   ") == 0

    def test_single_word(self):
        assert StringUtils.word_count("python") == 1

    def test_multiple_spaces(self):
        assert StringUtils.word_count("a  b   c") == 3

    def test_newlines(self):
        assert StringUtils.word_count("line one\nline two") == 4

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.word_count(["words"])


# ──────────────────────────────────────────────────────────────
# truncate()
# ──────────────────────────────────────────────────────────────
class TestTruncate:
    def test_no_truncation_needed(self):
        assert StringUtils.truncate("hello", 10) == "hello"

    def test_exact_length(self):
        assert StringUtils.truncate("hello", 5) == "hello"

    def test_truncation_applied(self):
        result = StringUtils.truncate("hello world", 8)
        assert result == "hello..."
        assert len(result) == 8

    def test_custom_suffix(self):
        result = StringUtils.truncate("hello world", 7, suffix="!")
        assert result.endswith("!")

    def test_zero_max_length(self):
        result = StringUtils.truncate("hello", 0)
        assert len(result) == 0

    def test_suffix_longer_than_max(self):
        result = StringUtils.truncate("hello world", 2, suffix="...")
        assert len(result) <= 3  # suffix trimmed

    def test_negative_max_length(self):
        with pytest.raises(ValueError):
            StringUtils.truncate("hello", -1)

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.truncate(123, 5)


# ──────────────────────────────────────────────────────────────
# caesar_cipher()
# ──────────────────────────────────────────────────────────────
class TestCaesarCipher:
    def test_basic_shift(self):
        assert StringUtils.caesar_cipher("abc", 1) == "bcd"

    def test_wrap_around(self):
        assert StringUtils.caesar_cipher("xyz", 3) == "abc"

    def test_uppercase_preserved(self):
        assert StringUtils.caesar_cipher("ABC", 1) == "BCD"

    def test_non_alpha_unchanged(self):
        assert StringUtils.caesar_cipher("Hello, World!", 13) == "Uryyb, Jbeyq!"

    def test_zero_shift(self):
        assert StringUtils.caesar_cipher("hello", 0) == "hello"

    def test_negative_shift(self):
        assert StringUtils.caesar_cipher("bcd", -1) == "abc"

    def test_full_alphabet_shift(self):
        assert StringUtils.caesar_cipher("hello", 26) == "hello"

    def test_empty_string(self):
        assert StringUtils.caesar_cipher("", 5) == ""

    def test_type_error_text(self):
        with pytest.raises(TypeError):
            StringUtils.caesar_cipher(123, 1)

    def test_type_error_shift(self):
        with pytest.raises(TypeError):
            StringUtils.caesar_cipher("abc", 1.5)


# ──────────────────────────────────────────────────────────────
# extract_emails()
# ──────────────────────────────────────────────────────────────
class TestExtractEmails:
    def test_single_email(self):
        assert StringUtils.extract_emails("Contact us at info@example.com") == ["info@example.com"]

    def test_multiple_emails(self):
        text = "Send to a@b.com and c@d.org"
        assert StringUtils.extract_emails(text) == ["a@b.com", "c@d.org"]

    def test_no_emails(self):
        assert StringUtils.extract_emails("No emails here!") == []

    def test_empty_string(self):
        assert StringUtils.extract_emails("") == []

    def test_email_with_subdomain(self):
        result = StringUtils.extract_emails("user@mail.example.co.uk")
        assert "user@mail.example.co.uk" in result

    def test_email_with_plus(self):
        result = StringUtils.extract_emails("user+tag@example.com")
        assert "user+tag@example.com" in result

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.extract_emails(None)


# ──────────────────────────────────────────────────────────────
# to_snake_case()
# ──────────────────────────────────────────────────────────────
class TestToSnakeCase:
    def test_camel_case(self):
        assert StringUtils.to_snake_case("CamelCase") == "camel_case"

    def test_lower_camel(self):
        assert StringUtils.to_snake_case("myVariableName") == "my_variable_name"

    def test_spaces(self):
        assert StringUtils.to_snake_case("hello world") == "hello_world"

    def test_hyphens(self):
        assert StringUtils.to_snake_case("hello-world") == "hello_world"

    def test_already_snake(self):
        assert StringUtils.to_snake_case("snake_case") == "snake_case"

    def test_all_uppercase(self):
        result = StringUtils.to_snake_case("ABC")
        assert result == result.lower()

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.to_snake_case(42)


# ──────────────────────────────────────────────────────────────
# count_vowels()
# ──────────────────────────────────────────────────────────────
class TestCountVowels:
    def test_basic(self):
        assert StringUtils.count_vowels("hello") == 2

    def test_uppercase_counted(self):
        assert StringUtils.count_vowels("AEIOU") == 5

    def test_no_vowels(self):
        assert StringUtils.count_vowels("rhythm") == 0

    def test_empty_string(self):
        assert StringUtils.count_vowels("") == 0

    def test_mixed(self):
        assert StringUtils.count_vowels("Python Testing") == 3  # o, e, i

    def test_type_error(self):
        with pytest.raises(TypeError):
            StringUtils.count_vowels(100)
