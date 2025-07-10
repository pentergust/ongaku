"""Playlist Impl's.

The playlist implemented classes.

TODO: Change Playlist to BasePlaylist
TODO: Change PlaylistInfo to BasePlaylistInfo
TODO: Change Track to BaseTrack
"""

import typing

from ongaku.abc import playlist as playlist_
from ongaku.abc import track as track_

__all__ = ("Playlist", "PlaylistInfo")


class Playlist(playlist_.Playlist):
    def __init__(
        self,
        info: playlist_.PlaylistInfo,
        tracks: typing.Sequence[track_.Track],
        plugin_info: typing.Mapping[str, typing.Any],
    ) -> None:
        self._info = info
        self._tracks = tracks
        self._plugin_info = plugin_info


class PlaylistInfo(playlist_.PlaylistInfo):
    def __init__(self, name: str, selected_track: int) -> None:
        self._name = name
        self._selected_track = selected_track
