"""Info Impl's.

The info implemented classes.
"""

import datetime
import typing

import hikari

from ongaku.impl.filters import Filters
from ongaku.impl.payload import PayloadObject
from ongaku.impl.track import Track

__all__ = ("Player", "State", "Voice")


class State(PayloadObject):
    """
    Players State.

    All the information for the players current state.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-state)
    """

    __slots__: typing.Sequence[str] = (
        "_connected",
        "_ping",
        "_position",
        "_time",
    )

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

    @property
    def time(self) -> datetime.datetime:
        """The current datetime."""
        return self._time

    @property
    def position(self) -> int:
        """The position of the track in milliseconds."""
        return self._position

    @property
    def connected(self) -> bool:
        """Whether Lavalink is connected to the voice gateway."""
        return self._connected

    @property
    def ping(self) -> int:
        """The ping of the session to the Discord voice server in milliseconds (-1 if not connected)."""
        return self._ping

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False

        if self.time != other.time:
            return False

        if self.position != other.position:
            return False

        if self.connected != other.connected:
            return False

        return self.ping == other.ping


class Voice(PayloadObject):
    """
    Players Voice state.

    All of the Player Voice information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#voice-state)
    """

    __slots__: typing.Sequence[str] = (
        "_endpoint",
        "_session_id",
        "_token",
    )

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

    @property
    def token(self) -> str:
        """The Discord voice token to authenticate with."""
        return self._token

    @property
    def endpoint(self) -> str:
        """The Discord voice endpoint to connect to."""
        return self._endpoint

    @property
    def session_id(self) -> str:
        """The Discord voice session id to authenticate with."""
        return self._session_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Voice):
            return False

        if self.token != other.token:
            return False

        if self.endpoint != other.endpoint:
            return False

        return self.session_id == other.session_id


class Player(PayloadObject):
    """
    Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#player)
    """

    __slots__: typing.Sequence[str] = (
        "_filters",
        "_guild_id",
        "_is_paused",
        "_state",
        "_track",
        "_voice",
        "_volume",
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
        """The volume of the player."""
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        if self.volume != other.volume:
            return False

        if self.is_paused != other.is_paused:
            return False

        if self.state != other.state:
            return False

        if self.voice != other.voice:
            return False

        return self.filters == other.filters
