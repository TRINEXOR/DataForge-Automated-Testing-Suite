"""
DataForge - A Python utility library for data processing, validation, and transformation.
Covers string manipulation, mathematical operations, and data parsing.
"""

from .string_utils import StringUtils
from .math_utils import MathUtils
from .data_parser import DataParser

__version__ = "1.0.0"
__all__ = ["StringUtils", "MathUtils", "DataParser"]
