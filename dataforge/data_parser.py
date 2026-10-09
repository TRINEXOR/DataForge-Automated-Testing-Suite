"""
data_parser.py - Data parsing and validation utilities for DataForge.
"""

import csv
import json
import io
from typing import Any, Dict, List, Optional


class DataParser:
    """Utilities for parsing and validating structured data."""

    @staticmethod
    def parse_csv(csv_text: str, delimiter: str = ",") -> List[Dict[str, str]]:
        """
        Parse a CSV string into a list of dictionaries.

        Args:
            csv_text: Raw CSV string (first row assumed to be header).
            delimiter: Field delimiter character.

        Returns:
            List of dicts mapping header names to values.
        """
        if not isinstance(csv_text, str):
            raise TypeError(f"Expected str, got {type(csv_text).__name__}")
        if not csv_text.strip():
            return []
        reader = csv.DictReader(io.StringIO(csv_text), delimiter=delimiter)
        return [dict(row) for row in reader]

    @staticmethod
    def parse_json(json_text: str) -> Any:
        """
        Parse a JSON string and return the corresponding Python object.

        Args:
            json_text: Valid JSON string.

        Returns:
            Parsed Python object.

        Raises:
            ValueError: If json_text is not valid JSON.
        """
        if not isinstance(json_text, str):
            raise TypeError(f"Expected str, got {type(json_text).__name__}")
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

    @staticmethod
    def flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
        """
        Flatten a nested dictionary using dot-notation keys.

        Args:
            d: Dictionary to flatten (may be nested).
            parent_key: Prefix for keys (used in recursion).
            sep: Separator inserted between key segments.

        Returns:
            Flat dictionary.
        """
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d).__name__}")
        items: Dict = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(DataParser.flatten_dict(v, new_key, sep))
            else:
                items[new_key] = v
        return items

    @staticmethod
    def validate_schema(data: Dict, schema: Dict) -> List[str]:
        """
        Validate a dictionary against a simple schema.

        Schema format:
            { "field_name": {"type": <type>, "required": bool, "min": num, "max": num} }

        Returns:
            List of validation error messages (empty list = valid).
        """
        errors: List[str] = []
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        if not isinstance(schema, dict):
            raise TypeError("schema must be a dict")

        for field, rules in schema.items():
            required = rules.get("required", False)
            expected_type = rules.get("type")

            if field not in data:
                if required:
                    errors.append(f"Missing required field: '{field}'")
                continue

            value = data[field]

            if expected_type and not isinstance(value, expected_type):
                errors.append(
                    f"Field '{field}': expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
                continue

            if isinstance(value, (int, float)):
                if "min" in rules and value < rules["min"]:
                    errors.append(
                        f"Field '{field}': value {value} is below minimum {rules['min']}"
                    )
                if "max" in rules and value > rules["max"]:
                    errors.append(
                        f"Field '{field}': value {value} exceeds maximum {rules['max']}"
                    )

            if isinstance(value, str):
                if "min_length" in rules and len(value) < rules["min_length"]:
                    errors.append(
                        f"Field '{field}': length {len(value)} is below minimum {rules['min_length']}"
                    )
                if "max_length" in rules and len(value) > rules["max_length"]:
                    errors.append(
                        f"Field '{field}': length {len(value)} exceeds maximum {rules['max_length']}"
                    )

        return errors

    @staticmethod
    def group_by(records: List[Dict], key: str) -> Dict[Any, List[Dict]]:
        """
        Group a list of dictionaries by a specified key.

        Args:
            records: List of dictionaries.
            key: The key to group by.

        Returns:
            Dict mapping key values to lists of matching records.
        """
        if not isinstance(records, list):
            raise TypeError("records must be a list")
        result: Dict[Any, List[Dict]] = {}
        for record in records:
            if not isinstance(record, dict):
                raise TypeError("Each record must be a dict")
            if key not in record:
                raise KeyError(f"Key '{key}' not found in record: {record}")
            group_val = record[key]
            result.setdefault(group_val, []).append(record)
        return result
