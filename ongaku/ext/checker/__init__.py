"""Checker.

Allows for you to check if a string is a link or a query.
"""

from .abc import Checked
from .abc import CheckedType
from .checker import check

__all__ = ("Checked", "CheckedType", "check")
