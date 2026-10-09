# DataForge — Automated Testing Suite (Week 3 Task)

## Overview

**DataForge** is a Python utility library covering three domains:

| Module | Class | Functions |
|---|---|---|
| `dataforge/string_utils.py` | `StringUtils` | `reverse`, `is_palindrome`, `word_count`, `truncate`, `caesar_cipher`, `extract_emails`, `to_snake_case`, `count_vowels` |
| `dataforge/math_utils.py` | `MathUtils` | `factorial`, `is_prime`, `gcd`, `lcm`, `mean`, `median`, `fibonacci`, `clamp` |
| `dataforge/data_parser.py` | `DataParser` | `parse_csv`, `parse_json`, `flatten_dict`, `validate_schema`, `group_by` |

---

## Project Structure

```
week3_task/
├── dataforge/
│   ├── __init__.py
│   ├── string_utils.py
│   ├── math_utils.py
│   └── data_parser.py
├── tests/
│   ├── __init__.py
│   ├── test_string_utils.py   (63 tests)
│   ├── test_math_utils.py     (61 tests)
│   ├── test_data_parser.py    (40 tests)
│   └── test_integration.py   (10 tests)
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.9 or higher  
- pytest >= 7.0  
- pytest-cov >= 4.0  

---

## How to Run the Tests

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run all tests
```bash
pytest
```

### 3. Run with coverage report
```bash
pytest --cov=dataforge --cov-report=term-missing
```

### 4. Run a specific test file
```bash
pytest tests/test_string_utils.py -v
```

### 5. Run a specific test class
```bash
pytest tests/test_math_utils.py::TestFactorial -v
```

---

## Test Summary

**Total: 174 tests — 174 passed, 0 failed**

| File | Tests | Description |
|---|---|---|
| `test_string_utils.py` | 63 | Unit tests for all StringUtils methods |
| `test_math_utils.py` | 61 | Unit tests for all MathUtils methods |
| `test_data_parser.py` | 40 | Unit tests for all DataParser methods |
| `test_integration.py` | 10 | Cross-module integration scenarios |

---

## Test Case Documentation

### StringUtils Tests

#### `TestReverse` (9 tests)
- Regular string, single char, empty string
- Palindrome (output equals input), string with spaces, numeric string, special characters
- TypeError on non-string inputs (int, None)

#### `TestIsPalindrome` (9 tests)
- Standard palindromes and non-palindromes
- Case-insensitive matching (default)
- Space-ignored matching ("a man a plan a canal panama")
- Single char and empty string edge cases
- Case-sensitive and space-sensitive mode flags
- TypeError on wrong type

#### `TestWordCount` (7 tests)
- Normal sentence, empty string, whitespace-only, single word
- Multiple consecutive spaces (all treated as one delimiter)
- Newline-separated words
- TypeError on list input

#### `TestTruncate` (8 tests)
- String shorter than max (no truncation), exact length
- Truncation with default "..." suffix, custom suffix
- Zero max_length, suffix longer than max_length
- ValueError on negative max_length; TypeError on non-string

#### `TestCaesarCipher` (10 tests)
- Basic forward shift, wrap-around at end of alphabet
- Uppercase preserved, non-alpha characters unchanged
- Zero shift (identity), negative shift (decrypt)
- Full 26-shift (round-trip identity), empty string
- TypeError for non-string text and non-integer shift

#### `TestExtractEmails` (7 tests)
- Single email, multiple emails in one string
- No emails present, empty string
- Email with subdomain, email with + tag
- TypeError on None

#### `TestToSnakeCase` (7 tests)
- CamelCase, lowerCamelCase, space-separated, hyphen-separated
- Already-snake input (idempotent), all-uppercase
- TypeError on integer input

#### `TestCountVowels` (6 tests)
- Standard word, all-uppercase vowels, no vowels (rhythm)
- Empty string, mixed case sentence, TypeError

---

### MathUtils Tests

#### `TestFactorial` (7 tests)
- Base cases: 0! = 1, 1! = 1
- Small value (5! = 120) and large value (10! = 3628800)
- ValueError for negative input; TypeError for float and string

#### `TestIsPrime` (10 tests)
- Known primes: 2, 3; Known composite: 4
- Boundary cases: 0, 1, negative numbers
- Large prime (97), large composite (100)
- Batch test of first 10 primes; TypeError for float

#### `TestGcd` (8 tests)
- Standard case (gcd(12,8)=4), coprime numbers
- Same-number case (gcd(n,n)=n), one zero, both zero
- Negative inputs (gcd uses absolute values), large numbers
- TypeError for float argument

#### `TestLcm` (5 tests)
- Standard case, coprime numbers, zero input, same numbers, TypeError

#### `TestMean` (7 tests)
- Integer list, float list, single element, negative numbers
- ValueError for empty list; TypeError for non-list and non-numeric element

#### `TestMedian` (7 tests)
- Odd-length list (returns middle), even-length list (average of two middle)
- Single element, unsorted input (auto-sorted internally)
- ValueError for empty list; TypeError for non-numeric, non-list

#### `TestFibonacci` (7 tests)
- Zero terms → [], one term → [0], two terms → [0, 1]
- Ten terms (explicit expected list)
- ValueError for negative n; TypeError for float
- Mathematical property test: each element = sum of previous two

#### `TestClamp` (7 tests)
- Value within range, below min (clamps to min), above max (clamps to max)
- At exact min, at exact max, float values
- ValueError when min_val > max_val

---

### DataParser Tests

#### `TestParseCsv` (8 tests)
- Standard two-column CSV, empty string → empty list
- Whitespace-only → empty list, header-only → empty list
- Custom semicolon delimiter, quoted fields containing commas
- TypeError for non-string; single-column CSV

#### `TestParseJson` (9 tests)
- Dict, list, nested dict, boolean, null, number
- Empty object {}, ValueError for malformed JSON
- TypeError for dict input (non-string)

#### `TestFlattenDict` (7 tests)
- Flat dict (unchanged), one-level nesting, deep 3-level nesting
- Mixed flat + nested, custom separator ("/")
- Empty dict → {}; TypeError for list input

#### `TestValidateSchema` (12 tests)
- Valid data (no errors), missing required field
- Wrong type, below min, above max
- String too short, string too long
- Optional field absent (valid), optional field present (valid)
- Multiple simultaneous errors; TypeError for non-dict data and schema

#### `TestGroupBy` (7 tests)
- Standard grouping (2 Engineering, 1 Marketing)
- All records in same group, empty list → {}
- KeyError when key missing from a record
- TypeError for non-list records and non-dict element
- Preserves full record content in grouped output

---

### Integration Tests

#### `TestEmailProcessingPipeline` (4 tests)
Simulates a user-data processing pipeline: CSV parse → email extraction → schema validation → minor/adult grouping. Verifies StringUtils and DataParser work correctly in sequence.

#### `TestMathAndStringCombined` (3 tests)
- Uses fibonacci sequence as length targets for truncation
- Counts vowels only in strings with prime-length words
- Encrypts text with a prime-number shift, then decrypts to confirm round-trip identity

#### `TestJsonWorkflow` (3 tests)
Parses nested JSON → flattens dicts → validates schema → computes mean and median on scores → identifies high scorers. Exercises DataParser and MathUtils together.

---

## TDD Methodology

The module was built following **Test-Driven Development**:

1. **Red** — Test cases were written first for each function, specifying expected inputs, outputs, and error conditions before implementation.
2. **Green** — Implementation code was written minimally to make each test pass.
3. **Refactor** — After all tests passed, code was reviewed for clarity: type-hint coverage, docstrings, and consistent error-message patterns were added without breaking any tests.

One test-driven discovery during development: the initial `count_vowels` test expected 4 vowels in "Python Testing" but the correct count is 3 (o, e, i). The test was corrected during the Green phase — demonstrating how TDD catches specification errors early.
