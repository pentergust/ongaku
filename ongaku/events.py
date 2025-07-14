"""Error Impl's.

The error implemented classes.
"""

from __future__ import annotations

import enum
import typing
from dataclasses import dataclass

import hikari

from ongaku.errors import ExceptionError
from ongaku.errors import SeverityType
from ongaku.impl.payload import PayloadObject

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.impl.player import State
    from ongaku.impl.statistics import Cpu
    from ongaku.impl.statistics import FrameStatistics
    from ongaku.impl.statistics import Memory
    from ongaku.impl.track import Track
    from ongaku.session import Session


__all__ = ("OngakuEvent", "PayloadEvent", "ReadyEvent", "TrackEndReasonType")


class TrackEndReasonType(str, enum.Enum):
    """Track end reason type.

    The track end reason type for the track that was just playing.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket#track-end-reason)
    """

    FINISHED = "finished"
    """The track finished playing."""
    LOADFAILED = "loadFailed"
    """The track failed to load."""
    STOPPED = "stopped"
    """The track was stopped."""
    REPLACED = "replaced"
    """The track was replaced."""
    CLEANUP = "cleanup"
    """The track was cleaned up."""


@dataclass(frozen=True, slots=True, order=True)
class OngakuEvent(hikari.Event):
    """Ongaku Event.

    The base ongaku event, that adds the client and session to all events.
    """

    client: Client
    """The ongaku client attached to the event."""

    session: Session
    """The session attached to the event."""

    @property
    def app(self) -> hikari.RESTAware:
        """App instance for this application."""
        return self.session.app


@dataclass(frozen=True, slots=True, order=True)
class PayloadEvent(OngakuEvent):
    """Payload Event.

    The event that is dispatched each time a message is received from the websocket.
    """

    payload: str
    """The payload received."""


@dataclass(frozen=True, slots=True, order=True)
class ReadyEvent(OngakuEvent):
    """Ready Event.

    Dispatched by Lavalink upon successful connection and authorization. Contains fields determining if resuming was successful, as well as the session id.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    resumed: bool
    """Whether or not the session has been resumed, or is a new session."""

    session_id: str
    """The lavalink session id, for the current session."""


@dataclass(frozen=True, slots=True, order=True)
class PlayerUpdateEvent(OngakuEvent):
    """Player Update Event.

    Dispatched every x seconds (configurable in `application.yml`) with the current state of the player.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    state: State
    """The player state."""


@dataclass(frozen=True, slots=True, order=True)
class StatisticsEvent(OngakuEvent):
    """Statistics Event.

    A collection of statistics sent every minute.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-op)
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

    frame_statistics: FrameStatistics | None
    """The frame statistics of the session."""


@dataclass(frozen=True, slots=True, order=True)
class TrackStartEvent(OngakuEvent):
    """Track start event.

    Dispatched when a track starts playing.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    track: Track
    """The track related to this event."""


@dataclass(frozen=True, slots=True, order=True)
class TrackEndEvent(OngakuEvent):
    """Track end event.

    Dispatched when a track ends.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    track: Track
    """The track related to this event."""

    reason: TrackEndReasonType
    """The reason for the track ending."""


class TrackExceptionError(ExceptionError, PayloadObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(
        self,
        message: str | None,
        severity: SeverityType,
        cause: str,
    ):
        self._message = message
        self._severity = severity
        self._cause = cause

    @property
    def message(self) -> str | None:
        return self._message

    @property
    def severity(self) -> SeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "TrackExceptionError":
        """Build Track Exception from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return TrackExceptionError(
            payload.get("message", None),
            SeverityType(payload["severity"]),
            payload["cause"],
        )


@dataclass(frozen=True, slots=True, order=True)
class TrackExceptionEvent(OngakuEvent):
    """Track exception event.

    Dispatched when a track throws an exception.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    track: Track
    """The track related to this event."""

    exception: ExceptionError
    """The occurred exception."""


@dataclass(frozen=True, slots=True, order=True)
class TrackStuckEvent(OngakuEvent):
    """Track stuck event.

    Dispatched when a track gets stuck while playing.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    track: Track
    """The track related to this event."""

    threshold_ms: int
    """The threshold in milliseconds that was exceeded."""


@dataclass(frozen=True, slots=True, order=True)
class WebsocketClosedEvent(OngakuEvent):
    """Websocket Closed Event.

    Dispatched when an audio WebSocket (to Discord) is closed. This can happen for various reasons (normal and abnormal), e.g. when using an expired voice server update. 4xxx codes are usually bad. See the [Discord Docs](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes).

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    code: int
    """The error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""

    reason: str
    """The close reason."""

    by_remote: bool
    """Whether the connection was closed by Discord."""


@dataclass(frozen=True, slots=True, order=True)
class QueueEmptyEvent(OngakuEvent):
    """Queue empty event.

    Dispatched when the player finishes all the tracks in the queue.
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    old_track: Track
    """The track that was previously playing."""


@dataclass(frozen=True, slots=True, order=True)
class QueueNextEvent(OngakuEvent):
    """Queue next event.

    Dispatched when the player starts playing a new track.
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""

    track: Track
    """The track related to this event."""

    old_track: Track
    """The track that was previously playing."""
