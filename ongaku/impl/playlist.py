"""Playlist Impl's.

The playlist implemented classes.
"""

import typing

from ongaku.impl.payload import PayloadObject
from ongaku.impl.track import Track

__all__ = ("Playlist", "PlaylistInfo")


class PlaylistInfo(PayloadObject):
    """Playlist information.

    The playlist info object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#playlist-info)
    """

    __slots__ = ("_name", "_selected_track")

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

    @property
    def name(self) -> str:
        """The name of the playlist."""
        return self._name

    @property
    def selected_track(self) -> int:
        """The selected track of the playlist (`-1` if no track is selected)."""
        return self._selected_track

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlaylistInfo):
            return False

        if self.name != other.name:
            return False

        return self.selected_track == other.selected_track


class Playlist(PayloadObject):
    """
    Playlist.

    The playlist object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#playlist-result-data)
    """

    __slots__: typing.Sequence[str] = (
        "_info",
        "_plugin_info",
        "_tracks",
    )

    def __init__(
        self,
        info: PlaylistInfo,
        tracks: typing.Sequence[Track],
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
        tracks: list[Track] = []
        for track_payload in payload["tracks"]:
            tracks.append(Track.from_payload(track_payload))

        return Playlist(
            PlaylistInfo.from_payload(payload["info"]),
            tracks,
            payload["pluginInfo"],
        )

    @property
    def info(self) -> PlaylistInfo:
        """The info of the playlist."""
        return self._info

    @property
    def tracks(self) -> typing.Sequence[Track]:
        """The tracks in this playlist."""
        return self._tracks

    @property
    def plugin_info(self) -> typing.Mapping[str, typing.Any]:
        """Addition playlist info provided by plugins."""
        return self._plugin_info

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Playlist):
            return False

        if self.info != other.info:
            return False

        if self.tracks != other.tracks:
            return False

        return self.plugin_info == other.plugin_info
