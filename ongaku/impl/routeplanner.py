"""RoutePlanner Impl's.

The routeplanner implemented classes.
"""

from __future__ import annotations

import typing

from ongaku.abc import routeplanner as routeplanner_

if typing.TYPE_CHECKING:
    import datetime

__all__ = (
    "FailingAddress",
    "IPBlock",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
)


class RoutePlannerStatus(routeplanner_.RoutePlannerStatus):
    def __init__(
        self,
        cls: routeplanner_.RoutePlannerType,
        details: routeplanner_.RoutePlannerDetails,
    ) -> None:
        self._cls = cls
        self._details = details


class RoutePlannerDetails(routeplanner_.RoutePlannerDetails):
    def __init__(
        self,
        ip_block: routeplanner_.IPBlock,
        failing_addresses: typing.Sequence[routeplanner_.FailingAddress],
        rotate_index: str | None,
        ip_index: str | None,
        current_address: str | None,
        current_address_index: str | None,
        block_index: str | None,
    ) -> None:
        self._ip_block = ip_block
        self._failing_addresses = failing_addresses
        self._rotate_index = rotate_index
        self._ip_index = ip_index
        self._current_address = current_address
        self._current_address_index = current_address_index
        self._block_index = block_index


class IPBlock(routeplanner_.IPBlock):
    def __init__(self, type: routeplanner_.IPBlockType, size: str) -> None:
        self._type = type
        self._size = size


class FailingAddress(routeplanner_.FailingAddress):
    def __init__(
        self, address: str, timestamp: datetime.datetime, time: str
    ) -> None:
        self._address = address
        self._timestamp = timestamp
        self._time = time
