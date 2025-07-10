"""Logger.

All logger functions, and trace related items.

TODO: Change logging to loguru.
"""

import logging
import typing

__all__ = ("TRACE_LEVEL", "TRACE_NAME", "logger")

TRACE_LEVEL: typing.Final[int] = logging.DEBUG - 5
"""The trace level for ongaku."""
TRACE_NAME: typing.Final[str] = "TRACE_ONGAKU"
"""The trace name for ongaku."""

logger = logging.getLogger("ongaku")
