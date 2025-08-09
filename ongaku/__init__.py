"""A voice handling library for hikari.

GitHub: https://github.com/hikari-ongaku/hikari-ongaku
Docs: https://ongaku.mplaty.com
"""

from ongaku.__metadata__ import (
    __author__,
    __author_email__,
    __license__,
    __maintainer__,
    __url__,
    __version__,
)
from ongaku.client import Client
from ongaku.errors import (
    BuildError,
    ClientAliveError,
    ClientError,
    NoSessionsError,
    OngakuError,
    PlayerConnectError,
    PlayerError,
    PlayerMissingError,
    PlayerNotConnectedError,
    PlayerQueueError,
    RestEmptyError,
    RestError,
    RestExceptionError,
    RestRequestError,
    RestStatusError,
    SessionError,
    SessionHandlerError,
    SessionStartError,
    SeverityType,
    TimeoutError,
)
from ongaku.events import (
    PayloadEvent,
    PlayerUpdateEvent,
    QueueEmptyEvent,
    QueueNextEvent,
    ReadyEvent,
    StatisticsEvent,
    TrackEndEvent,
    TrackEndReasonType,
    TrackExceptionEvent,
    TrackStartEvent,
    TrackStuckEvent,
    WebsocketClosedEvent,
)
from ongaku.handler.abc import BaseSessionHandler
from ongaku.handler.base import SessionHandler
from ongaku.impl.filters import BandType, Filters
from ongaku.impl.info import Info
from ongaku.impl.playlist import Playlist
from ongaku.impl.routeplanner import IPBlockType, RoutePlannerType
from ongaku.impl.session import SessionStatus
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track
from ongaku.player import Player
from ongaku.session import Session

__all__ = (  # noqa: RUF022
    # metadata
    "__author__",
    "__author_email__",
    "__license__",
    "__maintainer__",
    "__url__",
    "__version__",
    # client
    "Client",
    # errors
    "BuildError",
    "ClientAliveError",
    "ClientError",
    "NoSessionsError",
    "OngakuError",
    "PlayerConnectError",
    "PlayerError",
    "PlayerMissingError",
    "PlayerNotConnectedError",
    "PlayerQueueError",
    "RestEmptyError",
    "RestError",
    "RestExceptionError",
    "RestRequestError",
    "RestStatusError",
    "SessionError",
    "SessionHandlerError",
    "SessionStartError",
    "SeverityType",
    "TimeoutError",
    # Events
    "PayloadEvent",
    "PlayerUpdateEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
    "ReadyEvent",
    "StatisticsEvent",
    "TrackEndEvent",
    "TrackEndReasonType",
    "TrackExceptionEvent",
    "TrackStartEvent",
    "TrackStuckEvent",
    "WebsocketClosedEvent",
    # Handlers
    "BaseSessionHandler",
    "SessionHandler",
    # Impl
    "BandType",
    "Filters",
    "Info",
    "Player",
    "Playlist",
    "RoutePlannerType",
    "IPBlockType",
    "SessionStatus",
    "Statistics",
    "Track",
    # player
    "Player",
    # Session
    "Session",
)
