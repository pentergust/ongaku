"""RoutePlanner Impl's.

The routeplanner implemented classes.
"""

import datetime
import enum
import typing
from dataclasses import dataclass

from ongaku.impl.payload import PayloadObject

__all__ = (
    "FailingAddress",
    "IPBlock",
    "IPBlockType",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
    "RoutePlannerType",
)


class RoutePlannerType(str, enum.Enum):
    """Route Planner Type.

    The type of routeplanner that the server is currently using.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#route-planner-types)
    """

    ROTATING_ROUTE_PLANNER = "RotatingIpRoutePlanner"
    """IP address used is switched on ban. Recommended for IPv4 blocks or IPv6 blocks smaller than a /64."""
    NANO_IP_ROUTE_PLANNER = "NanoIpRoutePlanner"
    """IP address used is switched on clock update. Use with at least 1 /64 IPv6 block."""
    ROTATING_NANO_IP_ROUTE_PLANNER = "RotatingNanoIpRoutePlanner"
    """IP address used is switched on clock update, rotates to a different /64 block on ban. Use with at least 2x /64 IPv6 blocks."""
    BALANCING_IP_ROUTE_PLANNER = "BalancingIpRoutePlanner"
    """IP address used is selected at random per request. Recommended for larger IP blocks."""


class IPBlockType(str, enum.Enum):
    """IP Block Type.

    The IP Block type, 4, or 6.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#ip-block-type)
    """

    INET_4_ADDRESS = "Inet4Address"
    """The ipv4 block type"""
    INET_6_ADDRESS = "Inet6Address"
    """The ipv6 block type"""


@dataclass(order=True, frozen=True, slots=True)
class IPBlock(PayloadObject):
    """Route Planner IP Block.

    All of the information about the IP Block.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#ip-block-object)
    """

    type: IPBlockType
    """The type of the ip block."""

    size: str
    """The size of the ip block."""

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
            IPBlockType(payload["type"]),
            payload["size"],
        )


@dataclass(order=True, frozen=True, slots=True)
class FailingAddress(PayloadObject):
    """Failing address.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#failing-address-object)
    """

    address: str
    """The failing address."""

    timestamp: datetime.datetime
    """The datetime object of when the address failed."""

    time: str
    """The timestamp when the address failed as a pretty string."""

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


@dataclass(order=True, frozen=True, slots=True)
class RoutePlannerDetails(PayloadObject):
    """Route Planner details.

    All of the information about the failing addresses.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#details-object)
    """

    ip_block: IPBlock
    """The ip block being used."""

    failing_addresses: typing.Sequence[FailingAddress]
    """The failing addresses."""

    rotate_index: str | None
    """The number of rotations."""

    ip_index: str | None
    """The current offset in the block."""

    current_address: str | None
    """The current address being used."""

    current_address_index: str | None
    """The current offset in the ip block."""

    block_index: str | None
    """The current offset in the ip block."""

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


@dataclass(order=True, frozen=True, slots=True)
class RoutePlannerStatus(PayloadObject):
    """Route Planner Status Object.

    The status of the route-planner.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#get-routeplanner-status)
    """

    cls: RoutePlannerType
    """The name of the RoutePlanner implementation being used by this server."""

    details: RoutePlannerDetails
    """The status details of the RoutePlanner."""

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
            RoutePlannerType(payload["class"]),
            RoutePlannerDetails.from_payload(payload["details"]),
        )
