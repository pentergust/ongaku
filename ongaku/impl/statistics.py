"""Statistics Impl's.

The statistics implemented classes.
"""

import typing
from dataclasses import dataclass

from ongaku.impl.payload import PayloadObject

__all__ = ("Cpu", "FrameStatistics", "Memory", "Statistics")


@dataclass(order=True, frozen=True, slots=True)
class Memory(PayloadObject):
    """Statistics Memory.

    All of the Statistics Memory information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#memory)
    """

    free: int
    """The amount of free memory in bytes."""

    used: int
    """The amount of used memory in bytes."""

    allocated: int
    """The amount of allocated memory in bytes."""

    reservable: int
    """The amount of reservable memory in bytes."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Memory":
        """Build Memory Statistics from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Memory(
            payload["free"],
            payload["used"],
            payload["allocated"],
            payload["reservable"],
        )


@dataclass(order=True, frozen=True, slots=True)
class Cpu(PayloadObject):
    """Statistics CPU.

    All of the Statistics CPU information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#cpu)
    """

    cores: int
    """The amount of cores the server has."""

    system_load: float
    """The system load of the server."""

    lavalink_load: float
    """The load of Lavalink on the server."""

    @classmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> "Cpu":
        """Build Cpu Statistics from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Cpu(
            payload["cores"], payload["systemLoad"], payload["lavalinkLoad"]
        )


@dataclass(order=True, frozen=True, slots=True)
class FrameStatistics(PayloadObject):
    """Statistics Frame Statistics.

    All of the Statistics frame statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#frame-stats)
    """

    sent: int
    """The amount of frames sent to Discord."""

    nulled: int
    """The amount of frames that were nulled."""

    deficit: int
    """The difference between sent frames and the expected amount of frames."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "FrameStatistics":
        """Build Frame Statistics from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return FrameStatistics(
            payload["sent"], payload["nulled"], payload["deficit"]
        )


@dataclass(order=True, frozen=True, slots=True)
class Statistics(PayloadObject):
    """Statistics.

    All of the Statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """

    players: int
    """The amount of players connected to the session."""

    playing_players: int
    """The amount of players playing a track."""

    uptime: int
    """The uptime of the session in milliseconds."""

    memory: Memory
    """The memory stats of the session."""

    cpu: Cpu
    """The CPU stats of the session."""

    frame_stats: FrameStatistics | None
    """The frame statistics of the session."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Statistics":
        """Build Statistics from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Statistics(
            payload["players"],
            payload["playingPlayers"],
            payload["uptime"],
            Memory.from_payload(payload["memory"]),
            Cpu.from_payload(payload["cpu"]),
            FrameStatistics.from_payload(payload["frameStats"])
            if payload.get("frameStats", None) is not None
            else None,
        )
