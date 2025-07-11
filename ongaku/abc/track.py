"""Track ABC's.

The tracks abstract classes.
"""

import typing

from typing_extensions import Self

if typing.TYPE_CHECKING:
    import hikari

from ongaku.abc.payload import PayloadObject

__all__ = ("Track", "TrackInfo")


class Track(PayloadObject):
    """
    Track.

    The base track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track)
    """

    __slots__: typing.Sequence[str] = (
        "_encoded",
        "_info",
        "_plugin_info",
        "_requestor",
        "_user_data",
    )

    @property
    def encoded(self) -> str:
        """The BASE-64 encoded track data."""
        return self._encoded

    @property
    def info(self) -> Self:
        """Information about the track."""
        return self._info

    @property
    def plugin_info(self) -> typing.Mapping[str, typing.Any]:
        """Additional track info provided by plugins."""
        return self._plugin_info

    @property
    def user_data(self) -> typing.Mapping[str, typing.Any]:
        """Additional track data.

        !!! warning
            If you store a value of any type under the name `ongaku_requestor` it will be overridden.
        """
        return self._user_data

    @property
    def requestor(self) -> hikari.Snowflake | None:
        """The person who requested this track."""
        return self._requestor

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Track):
            return False

        if self.encoded != other.encoded:
            return False

        if self.info != other.info:
            return False

        if self.plugin_info != other.plugin_info:
            return False

        if self.user_data != other.user_data:
            return False

        return self.requestor == other.requestor


class TrackInfo(PayloadObject):
    """
    Track information.

    All of the information about the track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track-info)
    """

    __slots__: typing.Sequence[str] = (
        "_artwork_url",
        "_author",
        "_identifier",
        "_is_seekable",
        "_is_stream",
        "_isrc",
        "_length",
        "_position",
        "_source_name",
        "_title",
        "_uri",
    )

    @property
    def identifier(self) -> str:
        """The track identifier."""
        return self._identifier

    @property
    def is_seekable(self) -> bool:
        """Whether the track is seekable."""
        return self._is_seekable

    @property
    def author(self) -> str:
        """The track author."""
        return self._author

    @property
    def length(self) -> int:
        """The track length in milliseconds."""
        return self._length

    @property
    def is_stream(self) -> bool:
        """Whether the track is a stream."""
        return self._is_stream

    @property
    def position(self) -> int:
        """The track position in milliseconds."""
        return self._position

    @property
    def title(self) -> str:
        """The track title."""
        return self._title

    @property
    def source_name(self) -> str:
        """The tracks source name."""
        return self._source_name

    @property
    def uri(self) -> str | None:
        """The track URI."""
        return self._uri

    @property
    def artwork_url(self) -> str | None:
        """The track artwork URL."""
        return self._artwork_url

    @property
    def isrc(self) -> str | None:
        """The track ISRC."""
        return self._isrc

    def __eq__(self, other: object) -> bool:  # noqa: C901
        if not isinstance(other, TrackInfo):
            return False

        if self.identifier != other.identifier:
            return False

        if self.is_seekable != other.is_seekable:
            return False

        if self.author != other.author:
            return False

        if self.length != other.length:
            return False

        if self.is_stream != other.is_stream:
            return False

        if self.position != other.position:
            return False

        if self.title != other.title:
            return False

        if self.source_name != other.source_name:
            return False

        if self.uri != other.uri:
            return False

        if self.artwork_url != other.artwork_url:
            return False

        return self.isrc == other.isrc
