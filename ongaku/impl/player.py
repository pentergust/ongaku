"""Info Impl's.

The info implemented classes.
"""

import datetime
import typing
from dataclasses import dataclass

import hikari

from ongaku.impl.filters import Filters
from ongaku.impl.payload import PayloadObject
from ongaku.impl.track import Track

__all__ = ("Player", "State", "Voice")


@dataclass(order=True, slots=True)
class State(PayloadObject):
    """Players State.

    All the information for the players current state.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-state)
    """

    time: datetime.datetime
    """The current datetime."""

    position: int
    """The position of the track in milliseconds."""

    connected: bool
    """Whether Lavalink is connected to the voice gateway."""

    ping: int
    """The ping of the session to the Discord voice server in milliseconds (-1 if not connected)."""

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

    @classmethod
    def empty(cls) -> "State":
        return State(datetime.datetime.fromtimestamp(0), 0, False, 1)


@dataclass(order=True, slots=True)
class Voice(PayloadObject):
    """Players Voice state.

    All of the Player Voice information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#voice-state)
    """

    token: str
    """The Discord voice token to authenticate with."""

    endpoint: str
    """The Discord voice endpoint to connect to."""

    session_id: str
    """The Discord voice session id to authenticate with."""

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

    @classmethod
    def empty(cls) -> "Voice":
        return Voice("", "", "")


# TODO: Return frozen or ...
# From: https://github.com/hikari-ongaku/ongaku/commit/a5431c3a7e5283e7d7179aabcbb6af87b5f1f55a
class Player(PayloadObject):
    """Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#player)
    """

    __slots__ = (
        "_guild_id",
        "_track",
        "_volume",
        "_is_paused",
        "_state",
        "_voice",
        "_filters",
    )

    def __init__(
        self,
        guild_id: hikari.Snowflake,
        track: Track | None,
        volume: int,
        is_paused: bool,
        state: State,
        voice: Voice,
        filters: Filters | None,
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._volume = volume
        self._is_paused = is_paused
        self._state = state
        self._voice = voice
        self._filters = filters

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild id this player is attached too."""
        return self._guild_id

    @property
    def track(self) -> Track | None:
        """The track the player is currently playing.

        !!! note
            If the track is `None` then there is no current track playing.
        """
        return self._track

    @property
    def volume(self) -> int:
        """The volume of the player.

        If `-1` the player has not been connected to lavalink and updated.
        """
        return self._volume

    @property
    def is_paused(self) -> bool:
        """Whether the player is paused."""
        return self._is_paused

    @property
    def state(self) -> State:
        """The player's state."""
        return self._state

    @property
    def voice(self) -> Voice:
        """The player's voice state."""
        return self._voice

    @property
    def filters(self) -> Filters | None:
        """The filter object."""
        return self._filters

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
            hikari.Snowflake(payload["guildId"]),
            Track.from_payload(payload["track"])
            if payload.get("track", None)
            else None,
            payload["volume"],
            payload["paused"],
            State.from_payload(payload["state"]),
            Voice.from_payload(payload["voice"]),
            Filters.from_payload(payload["filters"])
            if payload.get("filters", False)
            else None,
        )
