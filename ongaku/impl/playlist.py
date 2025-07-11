"""Playlist Impl's.

The playlist implemented classes.
"""

import typing
from dataclasses import dataclass

from ongaku.impl.payload import PayloadObject
from ongaku.impl.track import Track

__all__ = ("Playlist", "PlaylistInfo")


@dataclass(order=True, frozen=True, slots=True)
class PlaylistInfo(PayloadObject):
    """Playlist information.

    The playlist info object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#playlist-info)
    """

    name: str
    """The name of the playlist."""

    selected_track: int
    """The selected track of the playlist (`-1` if no track is selected)."""

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


@dataclass(order=True, frozen=True, slots=True)
class Playlist(PayloadObject):
    """Playlist.

    The playlist object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#playlist-result-data)
    """

    info: PlaylistInfo
    """The info of the playlist."""

    tracks: typing.Sequence[Track]
    """The tracks in this playlist."""

    plugin_info: typing.Mapping[str, typing.Any]
    """Addition playlist info provided by plugins."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Playlist":
        """Build Playlist from payload.

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
