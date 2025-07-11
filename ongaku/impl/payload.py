"""Payload objects."""

import typing
from abc import ABC
from abc import abstractmethod

import orjson
from typing_extensions import Self

__all__ = ("PayloadMappingT", "PayloadObject")

PayloadMappingT: typing.TypeAlias = (
    typing.Mapping[str, typing.Any] | str | bytes
)
"""Payload Mapping Type. 

Supports string, bytes, or a mapping.
"""


def _ensure_mapping(
    payload: PayloadMappingT,
) -> typing.Mapping[str, typing.Any]:
    if isinstance(payload, str | bytes):
        data: typing.Mapping[str, typing.Any] = orjson.loads(payload)
        if isinstance(data, typing.Sequence):
            raise TypeError("Mapping is required.")
        return data

    return payload


class PayloadObject(ABC):
    """Object can build from payload."""

    @classmethod
    @abstractmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> Self:
        """Build object instance from payload."""

    @classmethod
    def from_payload(cls, payload: PayloadMappingT) -> Self:
        """Build object instance from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return cls._from_payload(_ensure_mapping(payload))
