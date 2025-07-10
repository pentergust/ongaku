"""Session ABC's.

The session abstract classes.
"""

import abc
import enum
import typing

__all__ = ("Session", "SessionStatus")


class Session(abc.ABC):
    """
    Session information.

    All of the specified session information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#update-session)
    """

    __slots__: typing.Sequence[str] = ("_resuming", "_timeout")

    @property
    def resuming(self) -> bool:
        """Whether resuming is enabled for this session or not."""
        return self._resuming

    @property
    def timeout(self) -> int:
        """The timeout in seconds."""
        return self._timeout

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Session):
            return False

        if self.resuming != other.resuming:
            return False

        return self.timeout == other.timeout


class SessionStatus(int, enum.Enum):
    """
    Session Status.

    The status of the session.
    """

    NOT_CONNECTED = 0
    """Not connected to the lavalink server."""
    CONNECTED = 1
    """Successfully connected to the lavalink server."""
    FAILURE = 2
    """A failure occurred connecting to the lavalink server."""


class WebsocketOPCode(str, enum.Enum):
    READY = "ready"
    PLAYER_UPDATE = "playerUpdate"
    STATS = "stats"
    EVENT = "event"


class WebsocketEvent(str, enum.Enum):
    TRACK_START_EVENT = "TrackStartEvent"
    TRACK_END_EVENT = "TrackEndEvent"
    TRACK_EXCEPTION_EVENT = "TrackExceptionEvent"
    TRACK_STUCK_EVENT = "TrackStuckEvent"
    WEBSOCKET_CLOSED_EVENT = "WebSocketClosedEvent"
