"""Session Impl's.

The session implemented classes.
"""

import enum
import typing
from dataclasses import dataclass

from ongaku.impl.payload import PayloadObject

__all__ = ("Session", "SessionStatus")


class SessionStatus(int, enum.Enum):
    """Session Status.

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


@dataclass(order=True, frozen=True, slots=True)
class Session(PayloadObject):
    """Session information.

    All of the specified session information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#update-session)
    """

    resuming: bool
    """Whether resuming is enabled for this session or not."""

    timeout: int
    """The timeout in seconds."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Session":
        """Build Session from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Session(payload["resuming"], payload["timeout"])
