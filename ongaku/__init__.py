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
from ongaku.abc.errors import SeverityType
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.filters import BandType
from ongaku.abc.playlist import Playlist
from ongaku.abc.routeplanner import IPBlockType
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.abc.session import SessionStatus
from ongaku.abc.track import Track
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
from ongaku.errors import TimeoutError
from ongaku.events import PayloadEvent
from ongaku.events import PlayerUpdateEvent
from ongaku.events import QueueEmptyEvent
from ongaku.events import QueueNextEvent
from ongaku.events import ReadyEvent
from ongaku.events import StatisticsEvent
from ongaku.events import TrackEndEvent
from ongaku.events import TrackExceptionEvent
from ongaku.events import TrackStartEvent
from ongaku.events import TrackStuckEvent
from ongaku.events import WebsocketClosedEvent
from ongaku.impl.filters import Filters
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import TRACE_NAME
from ongaku.player import Player
from ongaku.session import Session

logging.addLevelName(TRACE_LEVEL, TRACE_NAME)

__all__ = (  # noqa: RUF022
    # .__metadata__
    "__author__",
    "__author_email__",
    "__maintainer__",
    "__license__",
    "__url__",
    "__version__",
    # .client
    "Client",
    # .player
    "Player",
    # .session
    "Session",
    # .enums
    "SeverityType",
    "TrackEndReasonType",
    "RoutePlannerType",
    "IPBlockType",
    "SessionStatus",
    # .errors
    "OngakuError",
    "RestError",
    "RestStatusError",
    "RestRequestError",
    "RestEmptyError",
    "RestExceptionError",
    "ClientError",
    "ClientAliveError",
    "SessionError",
    "SessionStartError",
    "SessionHandlerError",
    "NoSessionsError",
    "PlayerError",
    "PlayerConnectError",
    "PlayerQueueError",
    "PlayerMissingError",
    "BuildError",
    "TimeoutError",
    # .events
    "PayloadEvent",
    "ReadyEvent",
    "PlayerUpdateEvent",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
    # .filters
    "Filters",
    "BandType",
    # .track
    "Track",
    # .playlist
    "Playlist",
)
