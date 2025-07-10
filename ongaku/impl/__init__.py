"""Implementation.

All implementations of abstract classes.
"""

from __future__ import annotations

from ongaku.abc.filters import BandType
from ongaku.impl.filters import Filters
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.impl.info import Git
from ongaku.impl.info import Info
from ongaku.impl.info import Plugin
from ongaku.impl.info import Version
from ongaku.impl.player import Player
from ongaku.impl.player import State
from ongaku.impl.player import Voice
from ongaku.impl.playlist import Playlist
from ongaku.impl.playlist import PlaylistInfo
from ongaku.impl.routeplanner import FailingAddress
from ongaku.impl.routeplanner import IPBlock
from ongaku.impl.routeplanner import RoutePlannerDetails
from ongaku.impl.routeplanner import RoutePlannerStatus
from ongaku.impl.session import Session
from ongaku.impl.statistics import Cpu
from ongaku.impl.statistics import FrameStatistics
from ongaku.impl.statistics import Memory
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track
from ongaku.impl.track import TrackInfo

__all__ = (  # noqa: RUF022
    # .filters
    "BandType",
    "Filters",
    # .handlers
    "BasicSessionHandler",
    # .info
    "Info",
    "Version",
    "Git",
    "Plugin",
    # .player
    "Player",
    "State",
    "Voice",
    # .playlist
    "Playlist",
    "PlaylistInfo",
    # .routeplanner
    "RoutePlannerStatus",
    "RoutePlannerDetails",
    "IPBlock",
    "FailingAddress",
    # .session
    "Session",
    # .statistics
    "Statistics",
    "Memory",
    "Cpu",
    "FrameStatistics",
    # .track
    "Track",
    "TrackInfo",
)
