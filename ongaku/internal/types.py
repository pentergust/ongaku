"""Types.

All types used in ongaku.

TODO: Move types to implementation
"""

import typing

import hikari

__all__ = ("RequestT", "RequestorT")

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


RequestorT: typing.TypeAlias = (
    hikari.SnowflakeishOr[hikari.User] | hikari.SnowflakeishOr[hikari.Member]
)
"""Requestor Type.

The types to set for a requestor of a track.s
"""
