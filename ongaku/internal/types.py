"""Types.

All types used in ongaku.
"""

import typing

import hikari

__all__ = ("PayloadMappingT", "PayloadSequenceT", "RequestT", "RequestorT")

# Generics
# ========

RequestT = typing.TypeVar(
    "RequestT",
    str,
    int,
    bool,
    float,
    dict[str, typing.Any],
    list[typing.Any],
    tuple[typing.Any, ...],
)
"""Request Type.

The types you can request for.
"""


# Type Aliases
# ============

RequestorT: typing.TypeAlias = (
    hikari.SnowflakeishOr[hikari.User] | hikari.SnowflakeishOr[hikari.Member]
)
"""Requestor Type.

The types to set for a requestor of a track.s
"""

PayloadMappingT: typing.TypeAlias = (
    typing.Mapping[str, typing.Any] | str | bytes
)
"""Payload Mapping Type. 

Supports string, bytes, or a mapping.
"""

PayloadSequenceT: typing.TypeAlias = typing.Sequence[typing.Any] | str | bytes
"""Payload Sequence Type. 

Supports string, bytes, or a sequence.
"""
