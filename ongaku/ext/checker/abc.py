"""Checker.

A extension, that checks if your query, is a track/playlist, or just a query.
"""

from enum import IntEnum


class CheckedType(IntEnum):
    """Checked type.

    The type of result you have received.
    """

    QUERY = 0
    """The result was a query."""
    TRACK = 1
    """The result was a track."""
    PLAYLIST = 2
    """The result was a playlist."""


class Checked:
    """Checked value.

    The checked, and confirmed value, with its specific type attached.
    """

    __slots__ = ("_type", "_value")

    def __init__(self, value: str, type: CheckedType) -> None:
        self._value = value
        self._type = type

    @property
    def value(self) -> str:
        """
        The value.

        This is the value, based on the [type][ongaku.ext.checker.abc.CheckedType] it is.
        """
        return self._value

    @property
    def type(self) -> CheckedType:
        """The type of the checked value."""
        return self._type
