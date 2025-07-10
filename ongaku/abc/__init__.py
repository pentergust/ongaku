"""Abstract classes.

All of the abstract classes for Ongaku.
"""

from ongaku.abc.errors import ExceptionError
from ongaku.abc.errors import SeverityType
from ongaku.abc.events import OngakuEvent
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.filters import BandType
from ongaku.abc.filters import ChannelMix
from ongaku.abc.filters import Distortion
from ongaku.abc.filters import Equalizer
from ongaku.abc.filters import Filters
from ongaku.abc.filters import Karaoke
from ongaku.abc.filters import LowPass
from ongaku.abc.filters import Rotation
from ongaku.abc.filters import Timescale
from ongaku.abc.filters import Tremolo
from ongaku.abc.filters import Vibrato
from ongaku.abc.handler import SessionHandler
from ongaku.abc.info import Git
from ongaku.abc.info import Info
from ongaku.abc.info import Plugin
from ongaku.abc.info import Version
from ongaku.abc.player import Player
from ongaku.abc.player import State
from ongaku.abc.player import Voice
from ongaku.abc.playlist import Playlist
from ongaku.abc.playlist import PlaylistInfo
from ongaku.abc.routeplanner import FailingAddress
from ongaku.abc.routeplanner import IPBlock
from ongaku.abc.routeplanner import IPBlockType
from ongaku.abc.routeplanner import RoutePlannerDetails
from ongaku.abc.routeplanner import RoutePlannerStatus
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.abc.session import Session
from ongaku.abc.session import SessionStatus
from ongaku.abc.statistics import Cpu
from ongaku.abc.statistics import FrameStatistics
from ongaku.abc.statistics import Memory
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track
from ongaku.abc.track import TrackInfo

__all__ = (  # noqa: RUF022
    # .errors
    "ExceptionError",
    "SeverityType",
    # .events
    "OngakuEvent",
    "TrackEndReasonType",
    # .filters
    "Filters",
    "Equalizer",
    "Karaoke",
    "Timescale",
    "Tremolo",
    "Vibrato",
    "Rotation",
    "Distortion",
    "ChannelMix",
    "LowPass",
    "BandType",
    # .handler
    "SessionHandler",
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
    "PlaylistInfo",
    "Playlist",
    # .routeplanner
    "RoutePlannerStatus",
    "RoutePlannerDetails",
    "IPBlock",
    "FailingAddress",
    "RoutePlannerType",
    "IPBlockType",
    # .session
    "Session",
    "SessionStatus",
    # .statistics
    "Statistics",
    "Memory",
    "Cpu",
    "FrameStatistics",
    # .track
    "TrackInfo",
    "Track",
)
