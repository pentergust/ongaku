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


@dataclass(order=True, frozen=True, slots=True)
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


@dataclass(order=True, frozen=True, slots=True)
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


@dataclass(order=True, frozen=True, slots=True)
class Player(PayloadObject):
    """Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#player)
    """

    guild_id: hikari.Snowflake
    """The guild id this player is attached too."""

    track: Track | None
    """The track the player is currently playing.

    !!! note
        If the track is `None` then there is no current track playing.
    """

    volume: int
    """The volume of the player."""

    is_paused: bool
    """Whether the player is paused."""

    state: State
    """The player's state."""

    voice: Voice
    """The player's voice state."""

    filters: Filters | None
    """The filter object."""

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
