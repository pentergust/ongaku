"""Info Impl's.

The info implemented classes.
"""

import datetime
import typing

import hikari

from ongaku.abc import filters as filters_
from ongaku.abc import player as player_
from ongaku.abc import track as track_

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

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Player":
        """Build Player from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Player(
            hikari.Snowflake(int(payload["guildId"])),
            track_.Track.from_payload(payload["track"])
            if payload.get("track", None)
            else None,
            payload["volume"],
            payload["paused"],
            State.from_payload(payload["state"]),
            Voice.from_payload(payload["voice"]),
            filters_.Filters.from_payload(payload["filters"])
            if payload.get("filters", False)
            else None,
        )


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

    @classmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> "State":
        """Build Player State from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return State(
            datetime.datetime.fromtimestamp(
                int(payload["time"]) / 1000,
                datetime.timezone.utc,
            ),
            payload["position"],
            payload["connected"],
            payload["ping"],
        )


class Voice(player_.Voice):
    def __init__(self, token: str, endpoint: str, session_id: str) -> None:
        self._token = token
        self._endpoint = endpoint
        self._session_id = session_id

    @classmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> "Voice":
        """Build Player Voice from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Voice(
            payload["token"], payload["endpoint"], payload["sessionId"]
        )
