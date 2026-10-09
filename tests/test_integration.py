"""
test_integration.py
Integration tests for DataForge — tests that span multiple modules
working together to simulate realistic workflows.
"""

import pytest
from dataforge import StringUtils, MathUtils, DataParser


class TestEmailProcessingPipeline:
    """
    Integration scenario:
    Parse a CSV of user records → validate → extract emails → apply transformations.
    """

    CSV_DATA = """name,age,contact
Alice Johnson,28,Reach me at alice@example.com or alice@work.org
Bob Smith,35,bob.smith@company.net
Charlie,17,no_email_here
"""

    def test_parse_and_extract_emails(self):
        records = DataParser.parse_csv(self.CSV_DATA)
        emails = []
        for record in records:
            emails.extend(StringUtils.extract_emails(record["contact"]))
        assert "alice@example.com" in emails
        assert "alice@work.org" in emails
        assert "bob.smith@company.net" in emails

    def test_name_to_snake_case(self):
        records = DataParser.parse_csv(self.CSV_DATA)
        snake_names = [StringUtils.to_snake_case(r["name"]) for r in records]
        assert "alice_johnson" in snake_names
        assert "bob_smith" in snake_names

    def test_age_validation_with_schema(self):
        records = DataParser.parse_csv(self.CSV_DATA)
        schema = {
            "name": {"type": str, "required": True},
            "age": {"type": str, "required": True},   # CSV values are strings
        }
        for record in records:
            errors = DataParser.validate_schema(record, schema)
            assert errors == [], f"Unexpected errors: {errors}"

    def test_group_by_age_bracket(self):
        records = DataParser.parse_csv(self.CSV_DATA)
        for r in records:
            r["minor"] = "yes" if int(r["age"]) < 18 else "no"
        grouped = DataParser.group_by(records, "minor")
        assert len(grouped.get("yes", [])) == 1
        assert len(grouped.get("no", [])) == 2


class TestMathAndStringCombined:
    """
    Integration scenario:
    Generate numeric sequences → format results using string utilities.
    """

    def test_fibonacci_word_lengths(self):
        """Use fibonacci numbers as word-length targets for truncation."""
        fibs = MathUtils.fibonacci(7)   # [0,1,1,2,3,5,8]
        sentence = "The quick brown fox jumps over the lazy dog"
        results = []
        for length in fibs:
            if length > 0:
                results.append(StringUtils.truncate(sentence, length))
        assert all(len(r) <= max(fibs) for r in results)

    def test_prime_vowel_counts(self):
        """Count vowels in strings of prime length."""
        words = ["hi", "hey", "hello", "python", "testing", "dataforge"]
        prime_vowel_counts = []
        for w in words:
            if MathUtils.is_prime(len(w)):
                prime_vowel_counts.append((w, StringUtils.count_vowels(w)))
        # All collected words must have prime lengths
        for word, _ in prime_vowel_counts:
            assert MathUtils.is_prime(len(word))

    def test_caesar_cipher_with_prime_shift(self):
        """Encrypt text using the 5th prime number as the shift."""
        primes = [n for n in range(2, 50) if MathUtils.is_prime(n)]
        shift = primes[4]  # 11
        original = "Hello World"
        encrypted = StringUtils.caesar_cipher(original, shift)
        decrypted = StringUtils.caesar_cipher(encrypted, -shift)
        assert decrypted == original


class TestJsonWorkflow:
    """
    Integration scenario:
    Parse JSON → flatten → validate → aggregate statistics.
    """

    JSON_DATA = '''[
        {"user": {"name": "Alice", "score": 85}},
        {"user": {"name": "Bob",   "score": 92}},
        {"user": {"name": "Carol", "score": 78}}
    ]'''

    def test_parse_flatten_and_validate(self):
        records = DataParser.parse_json(self.JSON_DATA)
        flat_records = [DataParser.flatten_dict(r) for r in records]
        schema = {
            "user.name":  {"type": str, "required": True},
            "user.score": {"type": int, "required": True, "min": 0, "max": 100},
        }
        for flat in flat_records:
            errors = DataParser.validate_schema(flat, schema)
            assert errors == []

    def test_statistics_on_scores(self):
        records = DataParser.parse_json(self.JSON_DATA)
        scores = [r["user"]["score"] for r in records]
        mean_score = MathUtils.mean(scores)
        median_score = MathUtils.median(scores)
        assert 78 <= mean_score <= 92
        assert median_score == 85.0

    def test_high_scorer_detection(self):
        records = DataParser.parse_json(self.JSON_DATA)
        threshold = 90
        high_scorers = [r["user"]["name"] for r in records if r["user"]["score"] >= threshold]
        assert "Bob" in high_scorers
        assert "Alice" not in high_scorers
