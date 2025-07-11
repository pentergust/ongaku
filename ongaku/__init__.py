"""A voice handling library for hikari.

GitHub: https://github.com/hikari-ongaku/hikari-ongaku
Docs: https://ongaku.mplaty.com
"""

import logging

from ongaku.__metadata__ import __author__
from ongaku.__metadata__ import __author_email__
from ongaku.__metadata__ import __license__
from ongaku.__metadata__ import __maintainer__
from ongaku.__metadata__ import __url__
from ongaku.__metadata__ import __version__
from ongaku.client import Client
from ongaku.errors import BuildError
from ongaku.errors import ClientAliveError
from ongaku.errors import ClientError
from ongaku.errors import NoSessionsError
from ongaku.errors import OngakuError
from ongaku.errors import PlayerConnectError
from ongaku.errors import PlayerError
from ongaku.errors import PlayerMissingError
from ongaku.errors import PlayerQueueError
from ongaku.errors import RestEmptyError
from ongaku.errors import RestError
from ongaku.errors import RestExceptionError
from ongaku.errors import RestRequestError
from ongaku.errors import RestStatusError
from ongaku.errors import SessionError
from ongaku.errors import SessionHandlerError
from ongaku.errors import SessionStartError
from ongaku.errors import SeverityType
from ongaku.errors import TimeoutError
from ongaku.events import PayloadEvent
from ongaku.events import PlayerUpdateEvent
from ongaku.events import QueueEmptyEvent
from ongaku.events import QueueNextEvent
from ongaku.events import ReadyEvent
from ongaku.events import StatisticsEvent
from ongaku.events import TrackEndEvent
from ongaku.events import TrackEndReasonType
from ongaku.events import TrackExceptionEvent
from ongaku.events import TrackStartEvent
from ongaku.events import TrackStuckEvent
from ongaku.events import WebsocketClosedEvent
from ongaku.handler.abc import BaseSessionHandler
from ongaku.handler.base import SessionHandler
from ongaku.impl.filters import BandType
from ongaku.impl.filters import Filters
from ongaku.impl.info import Info
from ongaku.impl.playlist import Playlist
from ongaku.impl.routeplanner import IPBlockType
from ongaku.impl.routeplanner import RoutePlannerType
from ongaku.impl.session import SessionStatus
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import TRACE_NAME
from ongaku.player import Player
from ongaku.session import Session

logging.addLevelName(TRACE_LEVEL, TRACE_NAME)

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
    # logger
    "TRACE_LEVEL",
    "TRACE_NAME",
    # player
    "Player",
    # Session
    "Session",
)
