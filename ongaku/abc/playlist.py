"""Playlist ABC's.

The playlist abstract classes.
"""

import abc
import typing

if typing.TYPE_CHECKING:
    from ongaku.abc.track import Track

__all__ = ("Playlist", "PlaylistInfo")


class Playlist(abc.ABC):
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


class PlaylistInfo(abc.ABC):
    """
    Playlist information.

    The playlist info object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#playlist-info)
    """

    __slots__: typing.Sequence[str] = (
        "_name",
        "_selected_track",
    )

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
