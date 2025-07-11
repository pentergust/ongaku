"""Error Impl's.

The error implemented classes.
"""

from __future__ import annotations

import enum
import typing

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


class OngakuEvent(hikari.Event):
    """Ongaku Event.

    The base ongaku event, that adds the client and session to all events.
    """

    __slots__: typing.Sequence[str] = ("_app", "_client", "_session")
    _client: Client
    _session: Session
    _app: hikari.RESTAware

    @property
    def client(self) -> Client:
        """The ongaku client attached to the event."""
        return self._client

    @property
    def session(self) -> Session:
        """The session attached to the event."""
        return self._session

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OngakuEvent):
            return False

        if self.client != other.client:
            return False

        return self.session == other.session


class PayloadEvent(OngakuEvent):
    """Payload Event.

    The event that is dispatched each time a message is received from the websocket.
    """

    __slots__: typing.Sequence[str] = ("_payload",)

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        payload: str,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._payload = payload

    @classmethod
    def from_session(cls, session: Session, payload: str) -> "PayloadEvent":
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, payload)

    @property
    def payload(self) -> str:
        """The payload received."""
        return self._payload

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PayloadEvent):
            return False

        return self.payload == other.payload


class ReadyEvent(OngakuEvent):
    """Ready Event.

    Dispatched by Lavalink upon successful connection and authorization. Contains fields determining if resuming was successful, as well as the session id.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    __slots__: typing.Sequence[str] = ("_resumed", "_session_id")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        resumed: bool,
        session_id: str,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._resumed = resumed
        self._session_id = session_id

    @classmethod
    def from_session(
        cls,
        session: Session,
        resumed: bool,
        session_id: str,
    ) -> "ReadyEvent":
        """Build the [ReadyEvent][ongaku.events.ReadyEvent] with just a session."""
        return cls(session.app, session.client, session, resumed, session_id)

    @property
    def resumed(self) -> bool:
        """Whether or not the session has been resumed, or is a new session."""
        return self._resumed

    @property
    def session_id(self) -> str:
        """The lavalink session id, for the current session."""
        return self._session_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReadyEvent):
            return False

        if self.resumed != other.resumed:
            return False

        return self.session_id == other.session_id


class PlayerUpdateEvent(OngakuEvent):
    """Player Update Event.

    Dispatched every x seconds (configurable in `application.yml`) with the current state of the player.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    __slots__: typing.Sequence[str] = ("_guild_id", "_state")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        state: State,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._state = state

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        state: State,
    ) -> "PlayerUpdateEvent":
        """Build the [PlayerUpdateEvent][ongaku.events.PlayerUpdateEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, state)

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def state(self) -> State:
        """The player state."""
        return self._state

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayerUpdateEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        return self.state != other.state


class StatisticsEvent(OngakuEvent):
    """Statistics Event.

    A collection of statistics sent every minute.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-op)
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
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        players: int,
        playing_players: int,
        uptime: int,
        memory: Memory,
        cpu: Cpu,
        frame_statistics: FrameStatistics | None,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._players = players
        self._playing_players = playing_players
        self._uptime = uptime
        self._memory = memory
        self._cpu = cpu
        self._frame_statistics = frame_statistics

    @classmethod
    def from_session(
        cls,
        session: Session,
        players: int,
        playing_players: int,
        uptime: int,
        memory: Memory,
        cpu: Cpu,
        frame_statistics: FrameStatistics | None,
    ) -> "StatisticsEvent":
        """Build the [StatisticsEvent][ongaku.events.StatisticsEvent] with just a session."""
        return cls(
            session.app,
            session.client,
            session,
            players,
            playing_players,
            uptime,
            memory,
            cpu,
            frame_statistics,
        )

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


class TrackStartEvent(OngakuEvent):
    """Track start event.

    Dispatched when a track starts playing.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    __slots__: typing.Sequence[str] = ("_guild_id", "_track")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
    ) -> "TrackStartEvent":
        """Build the [TrackStartEvent][ongaku.events.TrackStartEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, track)

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrackStartEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        return self.track == other.track


class TrackEndEvent(OngakuEvent):
    """Track end event.

    Dispatched when a track ends.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    __slots__: typing.Sequence[str] = ("_guild_id", "_reason", "_track")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        reason: TrackEndReasonType,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._reason = reason

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        reason: TrackEndReasonType,
    ) -> "TrackEndEvent":
        """Build the [TrackEndEvent][ongaku.events.TrackEndEvent] with just a session."""
        return cls(
            session.app, session.client, session, guild_id, track, reason
        )

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    @property
    def reason(self) -> TrackEndReasonType:
        """The reason for the track ending."""
        return self._reason

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrackEndEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        return self.reason == other.reason


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


class TrackExceptionEvent(OngakuEvent):
    """Track exception event.

    Dispatched when a track throws an exception.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    __slots__: typing.Sequence[str] = ("_exception", "_guild_id", "_track")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        exception: ExceptionError,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._exception = exception

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        exception: ExceptionError,
    ) -> "TrackExceptionEvent":
        """Build the [TrackExceptionEvent][ongaku.events.TrackExceptionEvent] with just a session."""
        return cls(
            session.app, session.client, session, guild_id, track, exception
        )

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    @property
    def exception(self) -> ExceptionError:
        """The occurred exception."""
        return self._exception

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrackExceptionEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        return self.exception == other.exception


class TrackStuckEvent(OngakuEvent):
    """Track stuck event.

    Dispatched when a track gets stuck while playing.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    __slots__: typing.Sequence[str] = ("_guild_id", "_threshold_ms", "_track")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        threshold_ms: int,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._threshold_ms = threshold_ms

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        threshold_ms: int,
    ) -> "TrackStuckEvent":
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(
            session.app, session.client, session, guild_id, track, threshold_ms
        )

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    @property
    def threshold_ms(self) -> int:
        """The threshold in milliseconds that was exceeded."""
        return self._threshold_ms

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrackStuckEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        return self.threshold_ms == other.threshold_ms


class WebsocketClosedEvent(OngakuEvent):
    """Websocket Closed Event.

    Dispatched when an audio WebSocket (to Discord) is closed. This can happen for various reasons (normal and abnormal), e.g. when using an expired voice server update. 4xxx codes are usually bad. See the [Discord Docs](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes).

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    __slots__ = ("_by_remote", "_code", "_guild_id", "_reason")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        code: int,
        reason: str,
        by_remote: bool,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._code = code
        self._reason = reason
        self._by_remote = by_remote

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        code: int,
        reason: str,
        by_remote: bool,
    ) -> "WebsocketClosedEvent":
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(
            session.app,
            session.client,
            session,
            guild_id,
            code,
            reason,
            by_remote,
        )

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def code(self) -> int:
        """The error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
        return self._code

    @property
    def reason(self) -> str:
        """The close reason."""
        return self._reason

    @property
    def by_remote(self) -> bool:
        """Whether the connection was closed by Discord."""
        return self._by_remote

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WebsocketClosedEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.code != other.code:
            return False

        if self.reason != other.reason:
            return False

        return self.by_remote == other.by_remote


class QueueEmptyEvent(OngakuEvent):
    """Queue empty event.

    Dispatched when the player finishes all the tracks in the queue.
    """

    __slots__: typing.Sequence[str] = ("_guild_id", "_old_track")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        old_track: Track,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._old_track = old_track

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        old_track: Track,
    ) -> "QueueEmptyEvent":
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, old_track)

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def old_track(self) -> Track:
        """The track that was previously playing."""
        return self._old_track

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QueueEmptyEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        return self.old_track == other.old_track


class QueueNextEvent(OngakuEvent):
    """Queue next event.

    Dispatched when the player starts playing a new track.
    """

    __slots__: typing.Sequence[str] = ("_guild_id", "_old_track", "_track")

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        old_track: Track,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._old_track = old_track

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: Track,
        old_track: Track,
    ) -> "QueueNextEvent":
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(
            session.app, session.client, session, guild_id, track, old_track
        )

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    @property
    def old_track(self) -> Track:
        """The track that was previously playing."""
        return self._old_track

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QueueNextEvent):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        return self.old_track == other.old_track
