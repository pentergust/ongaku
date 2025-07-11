"""Statistics Impl's.

The statistics implemented classes.
"""

import typing

from ongaku.impl.payload import PayloadObject

__all__ = ("Cpu", "FrameStatistics", "Memory", "Statistics")


class Memory(PayloadObject):
    """Statistics Memory.

    All of the Statistics Memory information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#memory)
    """

    __slots__ = ("_allocated", "_free", "_reservable", "_used")

    def __init__(
        self, free: int, used: int, allocated: int, reservable: int
    ) -> None:
        self._free = free
        self._used = used
        self._allocated = allocated
        self._reservable = reservable

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

    @property
    def free(self) -> int:
        """The amount of free memory in bytes."""
        return self._free

    @property
    def used(self) -> int:
        """The amount of used memory in bytes."""
        return self._used

    @property
    def allocated(self) -> int:
        """The amount of allocated memory in bytes."""
        return self._allocated

    @property
    def reservable(self) -> int:
        """The amount of reservable memory in bytes."""
        return self._reservable

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Memory):
            return False

        if self.free != other.free:
            return False

        if self.used != other.used:
            return False

        if self.allocated != other.allocated:
            return False

        return self.reservable == other.reservable


class Cpu(PayloadObject):
    """Statistics CPU.

    All of the Statistics CPU information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#cpu)
    """

    __slots__ = ("_cores", "_lavalink_load", "_system_load")

    def __init__(
        self, cores: int, system_load: float, lavalink_load: float
    ) -> None:
        self._cores = cores
        self._system_load = system_load
        self._lavalink_load = lavalink_load

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

    @property
    def cores(self) -> int:
        """The amount of cores the server has."""
        return self._cores

    @property
    def system_load(self) -> float:
        """The system load of the server."""
        return self._system_load

    @property
    def lavalink_load(self) -> float:
        """The load of Lavalink on the server."""
        return self._lavalink_load

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cpu):
            return False

        if self.cores != other.cores:
            return False

        if self.system_load != other.system_load:
            return False

        return self.lavalink_load == other.lavalink_load


class FrameStatistics(PayloadObject):
    """
    Statistics Frame Statistics.

    All of the Statistics frame statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#frame-stats)
    """

    __slots__ = ("_deficit", "_nulled", "_sent")

    def __init__(self, sent: int, nulled: int, deficit: int) -> None:
        self._sent = sent
        self._nulled = nulled
        self._deficit = deficit

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

    @property
    def sent(self) -> int:
        """The amount of frames sent to Discord."""
        return self._sent

    @property
    def nulled(self) -> int:
        """The amount of frames that were nulled."""
        return self._nulled

    @property
    def deficit(self) -> int:
        """The difference between sent frames and the expected amount of frames."""
        return self._deficit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrameStatistics):
            return False

        if self.sent != other.sent:
            return False

        if self.nulled != other.nulled:
            return False

        return self.deficit == other.deficit


class Statistics(PayloadObject):
    """
    Statistics.

    All of the Statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """

    __slots__: typing.Sequence[str] = (
        "_cpu",
        "_frame_statistics",
        "_memory",
        "_players",
        "_playing_players",
        "_uptime",
    )

    def __init__(
        self,
        players: int,
        playing_players: int,
        uptime: int,
        memory: Memory,
        cpu: Cpu,
        frame_statistics: FrameStatistics | None,
    ) -> None:
        self._players = players
        self._playing_players = playing_players
        self._uptime = uptime
        self._memory = memory
        self._cpu = cpu
        self._frame_statistics = frame_statistics

    @property
    def players(self) -> int:
        """The amount of players connected to the session."""
        return self._players

    @property
    def playing_players(self) -> int:
        """The amount of players playing a track."""
        return self._playing_players

    @property
    def uptime(self) -> int:
        """The uptime of the session in milliseconds."""
        return self._uptime

    @property
    def memory(self) -> Memory:
        """The memory stats of the session."""
        return self._memory

    @property
    def cpu(self) -> Cpu:
        """The CPU stats of the session."""
        return self._cpu

    @property
    def frame_stats(self) -> FrameStatistics | None:
        """The frame statistics of the session."""
        return self._frame_statistics

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Statistics):
            return False

        if self.players != other.players:
            return False

        if self.playing_players != other.playing_players:
            return False

        if self.uptime != other.uptime:
            return False

        if self.memory != other.memory:
            return False

        if self.cpu != other.cpu:
            return False

        return self.frame_stats == other.frame_stats
