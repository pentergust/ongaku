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

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Playlist":
        """Build Playlist.

        Builds a [`Playlist`][ongaku.abc.playlist.Playlist] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        playlist_.Playlist
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        tracks: list[track_.Track] = []
        for track_payload in payload["tracks"]:
            tracks.append(track_.Track.from_payload(track_payload))

        return Playlist(
            PlaylistInfo.from_payload(payload["info"]),
            tracks,
            payload["pluginInfo"],
        )


class PlaylistInfo(playlist_.PlaylistInfo):
    def __init__(self, name: str, selected_track: int) -> None:
        self._name = name
        self._selected_track = selected_track

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "PlaylistInfo":
        """Build Playlist Info from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return PlaylistInfo(payload["name"], payload["selectedTrack"])
