"""Statistics Impl's.

The statistics implemented classes.
"""

from __future__ import annotations

import typing

from ongaku.abc import statistics as statistics_

__all__ = ("Cpu", "FrameStatistics", "Memory", "Statistics")


class Statistics(statistics_.Statistics):
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
        memory: statistics_.Memory,
        cpu: statistics_.Cpu,
        frame_statistics: statistics_.FrameStatistics | None,
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
    def memory(self) -> statistics_.Memory:
        """The memory stats of the session."""
        return self._memory

    @property
    def cpu(self) -> statistics_.Cpu:
        """The CPU stats of the session."""
        return self._cpu

    @property
    def frame_stats(self) -> statistics_.FrameStatistics | None:
        """The frame statistics of the session."""
        return self._frame_statistics


class Memory(statistics_.Memory):
    def __init__(
        self, free: int, used: int, allocated: int, reservable: int
    ) -> None:
        self._free = free
        self._used = used
        self._allocated = allocated
        self._reservable = reservable


class Cpu(statistics_.Cpu):
    def __init__(
        self, cores: int, system_load: float, lavalink_load: float
    ) -> None:
        self._cores = cores
        self._system_load = system_load
        self._lavalink_load = lavalink_load


class FrameStatistics(statistics_.FrameStatistics):
    def __init__(self, sent: int, nulled: int, deficit: int) -> None:
        self._sent = sent
        self._nulled = nulled
        self._deficit = deficit
