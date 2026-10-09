"""
test_data_parser.py
Unit tests for dataforge.DataParser
"""

import pytest
from dataforge.data_parser import DataParser


# ──────────────────────────────────────────────────────────────
# parse_csv()
# ──────────────────────────────────────────────────────────────
class TestParseCsv:
    def test_basic_csv(self):
        csv = "name,age\nAlice,30\nBob,25"
        result = DataParser.parse_csv(csv)
        assert len(result) == 2
        assert result[0] == {"name": "Alice", "age": "30"}
        assert result[1] == {"name": "Bob", "age": "25"}

    def test_empty_csv(self):
        assert DataParser.parse_csv("") == []

    def test_whitespace_only(self):
        assert DataParser.parse_csv("   ") == []

    def test_header_only(self):
        result = DataParser.parse_csv("col1,col2")
        assert result == []

    def test_custom_delimiter(self):
        csv = "name;age\nAlice;30"
        result = DataParser.parse_csv(csv, delimiter=";")
        assert result[0]["name"] == "Alice"

    def test_quoted_fields(self):
        csv = 'name,bio\nAlice,"Loves Python, testing"'
        result = DataParser.parse_csv(csv)
        assert result[0]["bio"] == "Loves Python, testing"

    def test_type_error(self):
        with pytest.raises(TypeError):
            DataParser.parse_csv(123)

    def test_single_column(self):
        result = DataParser.parse_csv("fruit\napple\nbanana")
        assert [r["fruit"] for r in result] == ["apple", "banana"]


# ──────────────────────────────────────────────────────────────
# parse_json()
# ──────────────────────────────────────────────────────────────
class TestParseJson:
    def test_dict(self):
        assert DataParser.parse_json('{"key": "value"}') == {"key": "value"}

    def test_list(self):
        assert DataParser.parse_json('[1, 2, 3]') == [1, 2, 3]

    def test_nested(self):
        data = DataParser.parse_json('{"a": {"b": 1}}')
        assert data["a"]["b"] == 1

    def test_boolean(self):
        assert DataParser.parse_json('true') is True

    def test_null(self):
        assert DataParser.parse_json('null') is None

    def test_number(self):
        assert DataParser.parse_json('42') == 42

    def test_invalid_json(self):
        with pytest.raises(ValueError):
            DataParser.parse_json("{bad json}")

    def test_empty_object(self):
        assert DataParser.parse_json('{}') == {}

    def test_type_error(self):
        with pytest.raises(TypeError):
            DataParser.parse_json({"key": "val"})


# ──────────────────────────────────────────────────────────────
# flatten_dict()
# ──────────────────────────────────────────────────────────────
class TestFlattenDict:
    def test_flat_dict_unchanged(self):
        d = {"a": 1, "b": 2}
        assert DataParser.flatten_dict(d) == {"a": 1, "b": 2}

    def test_one_level_nesting(self):
        d = {"a": {"b": 1}}
        assert DataParser.flatten_dict(d) == {"a.b": 1}

    def test_deep_nesting(self):
        d = {"a": {"b": {"c": 42}}}
        assert DataParser.flatten_dict(d) == {"a.b.c": 42}

    def test_mixed_nesting(self):
        d = {"x": 1, "y": {"z": 2}}
        result = DataParser.flatten_dict(d)
        assert result["x"] == 1
        assert result["y.z"] == 2

    def test_custom_separator(self):
        d = {"a": {"b": 1}}
        result = DataParser.flatten_dict(d, sep="/")
        assert "a/b" in result

    def test_empty_dict(self):
        assert DataParser.flatten_dict({}) == {}

    def test_type_error(self):
        with pytest.raises(TypeError):
            DataParser.flatten_dict([1, 2, 3])


# ──────────────────────────────────────────────────────────────
# validate_schema()
# ──────────────────────────────────────────────────────────────
class TestValidateSchema:
    SCHEMA = {
        "name": {"type": str, "required": True, "min_length": 1, "max_length": 50},
        "age":  {"type": int, "required": True, "min": 0, "max": 150},
        "email": {"type": str, "required": False},
    }

    def test_valid_data(self):
        data = {"name": "Alice", "age": 30}
        assert DataParser.validate_schema(data, self.SCHEMA) == []

    def test_missing_required_field(self):
        data = {"age": 25}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert any("name" in e for e in errors)

    def test_wrong_type(self):
        data = {"name": "Alice", "age": "thirty"}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert any("age" in e for e in errors)

    def test_below_min(self):
        data = {"name": "Alice", "age": -1}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert any("minimum" in e for e in errors)

    def test_above_max(self):
        data = {"name": "Alice", "age": 200}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert any("maximum" in e for e in errors)

    def test_string_too_short(self):
        data = {"name": "", "age": 25}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert any("name" in e for e in errors)

    def test_string_too_long(self):
        data = {"name": "A" * 51, "age": 25}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert any("name" in e for e in errors)

    def test_optional_field_absent(self):
        data = {"name": "Bob", "age": 20}
        assert DataParser.validate_schema(data, self.SCHEMA) == []

    def test_optional_field_present(self):
        data = {"name": "Bob", "age": 20, "email": "bob@example.com"}
        assert DataParser.validate_schema(data, self.SCHEMA) == []

    def test_multiple_errors(self):
        data = {"age": -5}
        errors = DataParser.validate_schema(data, self.SCHEMA)
        assert len(errors) >= 2  # missing name + age below min

    def test_type_error_data(self):
        with pytest.raises(TypeError):
            DataParser.validate_schema("not a dict", self.SCHEMA)

    def test_type_error_schema(self):
        with pytest.raises(TypeError):
            DataParser.validate_schema({"a": 1}, "not a dict")


# ──────────────────────────────────────────────────────────────
# group_by()
# ──────────────────────────────────────────────────────────────
class TestGroupBy:
    RECORDS = [
        {"dept": "Engineering", "name": "Alice"},
        {"dept": "Engineering", "name": "Bob"},
        {"dept": "Marketing", "name": "Carol"},
    ]

    def test_basic_grouping(self):
        result = DataParser.group_by(self.RECORDS, "dept")
        assert len(result["Engineering"]) == 2
        assert len(result["Marketing"]) == 1

    def test_all_same_group(self):
        records = [{"type": "A"}, {"type": "A"}]
        result = DataParser.group_by(records, "type")
        assert len(result["A"]) == 2

    def test_empty_list(self):
        assert DataParser.group_by([], "key") == {}

    def test_missing_key_raises(self):
        records = [{"dept": "Eng"}, {"name": "Bob"}]
        with pytest.raises(KeyError):
            DataParser.group_by(records, "dept")

    def test_type_error_records(self):
        with pytest.raises(TypeError):
            DataParser.group_by("not a list", "key")

    def test_type_error_record_element(self):
        with pytest.raises(TypeError):
            DataParser.group_by([{"a": 1}, "bad"], "a")

    def test_preserves_record_content(self):
        result = DataParser.group_by(self.RECORDS, "dept")
        eng_names = [r["name"] for r in result["Engineering"]]
        assert "Alice" in eng_names and "Bob" in eng_names
