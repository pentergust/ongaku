"""RoutePlanner Impl's.

The routeplanner implemented classes.
"""

import datetime
import enum
import typing

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


class IPBlock(PayloadObject):
    """
    Route Planner IP Block.

    All of the information about the IP Block.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#ip-block-object)
    """

    __slots__ = ("_size", "_type")

    def __init__(self, type: IPBlockType, size: str) -> None:
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
            IPBlockType(payload["type"]),
            payload["size"],
        )

    @property
    def type(self) -> IPBlockType:
        """The type of the ip block."""
        return self._type

    @property
    def size(self) -> str:
        """The size of the ip block."""
        return self._size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPBlock):
            return False

        if self.type != other.type:
            return False

        return self.size == other.size


class FailingAddress(PayloadObject):
    """Failing address.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#failing-address-object)
    """

    __slots__ = ("_address", "_time", "_timestamp")

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

    @property
    def address(self) -> str:
        """The failing address."""
        return self._address

    @property
    def timestamp(self) -> datetime.datetime:
        """The datetime object of when the address failed."""
        return self._timestamp

    @property
    def time(self) -> str:
        """The timestamp when the address failed as a pretty string."""
        return self._time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FailingAddress):
            return False

        if self.address != other.address:
            return False

        if self.timestamp != other.timestamp:
            return False

        return self.time == other.time


class RoutePlannerDetails(PayloadObject):
    """
    Route Planner details.

    All of the information about the failing addresses.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#details-object)
    """

    __slots__: typing.Sequence[str] = (
        "_block_index",
        "_current_address",
        "_current_address_index",
        "_failing_addresses",
        "_ip_block",
        "_ip_index",
        "_rotate_index",
    )

    def __init__(
        self,
        ip_block: IPBlock,
        failing_addresses: typing.Sequence[FailingAddress],
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

    @property
    def ip_block(self) -> IPBlock:
        """The ip block being used."""
        return self._ip_block

    @property
    def failing_addresses(self) -> typing.Sequence[FailingAddress]:
        """The failing addresses."""
        return self._failing_addresses

    @property
    def rotate_index(self) -> str | None:
        """The number of rotations."""
        return self._rotate_index

    @property
    def ip_index(self) -> str | None:
        """The current offset in the block."""
        return self._ip_index

    @property
    def current_address(self) -> str | None:
        """The current address being used."""
        return self._current_address

    @property
    def current_address_index(self) -> str | None:
        """The current offset in the ip block."""
        return self._current_address_index

    @property
    def block_index(self) -> str | None:
        """The current offset in the ip block."""
        return self._block_index

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RoutePlannerDetails):
            return False

        if self.ip_block != other.ip_block:
            return False

        if self.failing_addresses != other.failing_addresses:
            return False

        if self.rotate_index != other.rotate_index:
            return False

        if self.ip_index != other.ip_index:
            return False

        if self.current_address != other.current_address:
            return False

        if self.current_address_index != other.current_address_index:
            return False

        return self.block_index == other.block_index


class RoutePlannerStatus(PayloadObject):
    """
    Route Planner Status Object.

    The status of the route-planner.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#get-routeplanner-status)
    """

    __slots__: typing.Sequence[str] = ("_cls", "_details")

    def __init__(
        self,
        cls: RoutePlannerType,
        details: RoutePlannerDetails,
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
            RoutePlannerType(payload["class"]),
            RoutePlannerDetails.from_payload(payload["details"]),
        )

    @property
    def cls(self) -> RoutePlannerType:
        """The name of the RoutePlanner implementation being used by this server."""
        return self._cls

    @property
    def details(self) -> RoutePlannerDetails:
        """The status details of the RoutePlanner."""
        return self._details

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RoutePlannerStatus):
            return False

        if self.cls != other.cls:
            return False

        return self.details == other.details
