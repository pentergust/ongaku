"""Info Impl's.

The info implemented classes.
"""

import typing

from ongaku.abc import filters as filters_
from ongaku.abc import player as player_
from ongaku.abc import track as track_

if typing.TYPE_CHECKING:
    import datetime

    import hikari

__all__ = ("Player", "State", "Voice")


class Player(player_.Player):
    def __init__(
        self,
        guild_id: hikari.Snowflake,
        track: track_.Track | None,
        volume: int,
        is_paused: bool,
        state: player_.State,
        voice: player_.Voice,
        filters: filters_.Filters | None,
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._volume = volume
        self._is_paused = is_paused
        self._state = state
        self._voice = voice
        self._filters = filters


class State(player_.State):
    def __init__(
        self,
        time: datetime.datetime,
        position: int,
        connected: bool,
        ping: int,
    ) -> None:
        self._time = time
        self._position = position
        self._connected = connected
        self._ping = ping


class Voice(player_.Voice):
    def __init__(self, token: str, endpoint: str, session_id: str) -> None:
        self._token = token
        self._endpoint = endpoint
        self._session_id = session_id
