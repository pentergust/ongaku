"""RoutePlanner Impl's.

The routeplanner implemented classes.
"""

import datetime
import typing

from ongaku.abc import routeplanner as routeplanner_

__all__ = (
    "FailingAddress",
    "IPBlock",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
)


class IPBlock(routeplanner_.IPBlock):
    def __init__(self, type: routeplanner_.IPBlockType, size: str) -> None:
        self._type = type
        self._size = size

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "IPBlock":
        """Build Route Planner IP Block from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return IPBlock(
            routeplanner_.IPBlockType(payload["type"]),
            payload["size"],
        )


class FailingAddress(routeplanner_.FailingAddress):
    def __init__(
        self, address: str, timestamp: datetime.datetime, time: str
    ) -> None:
        self._address = address
        self._timestamp = timestamp
        self._time = time

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "FailingAddress":
        """Build Route Planner Details from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return FailingAddress(
            payload["failingAddress"],
            datetime.datetime.fromtimestamp(
                int(payload["failingTimestamp"]) / 1000,
                datetime.timezone.utc,
            ),
            payload["failingTime"],
        )


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

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "RoutePlannerDetails":
        """Build Route Planner Details from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        failing_addresses: list[FailingAddress] = []
        for failing_address in payload["failingAddresses"]:
            failing_addresses.append(
                FailingAddress.from_payload(failing_address),
            )

        return RoutePlannerDetails(
            IPBlock.from_payload(payload["ipBlock"]),
            failing_addresses,
            payload.get("rotateIndex", None),
            payload.get("ipIndex", None),
            payload.get("currentAddress", None),
            payload.get("currentAddressIndex", None),
            payload.get("blockIndex", None),
        )


class RoutePlannerStatus(routeplanner_.RoutePlannerStatus):
    def __init__(
        self,
        cls: routeplanner_.RoutePlannerType,
        details: routeplanner_.RoutePlannerDetails,
    ) -> None:
        self._cls = cls
        self._details = details

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "RoutePlannerStatus":
        """Build Route Planner Status from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return RoutePlannerStatus(
            routeplanner_.RoutePlannerType(payload["class"]),
            RoutePlannerDetails.from_payload(payload["details"]),
        )
