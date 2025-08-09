"""Track Impl's.

The track implemented classes.
"""

import typing
from dataclasses import dataclass

import hikari

from ongaku.impl.payload import PayloadObject

__all__ = ("Track", "TrackInfo")


@dataclass(order=True, frozen=True, slots=True)
class TrackInfo(PayloadObject):
    """Track information.

    All of the information about the track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track-info)
    """

    identifier: str
    """The track identifier."""

    is_seekable: bool
    """Whether the track is seekable."""

    author: str
    """The track author."""

    length: int
    """The track length in milliseconds."""

    is_stream: bool
    """Whether the track is a stream."""

    position: int
    """The track position in milliseconds."""

    title: str
    """The track title."""

    source_name: str
    """The tracks source name."""

    uri: str | None
    """The track URI."""

    artwork_url: str | None
    """The track artwork URL."""

    isrc: str | None
    """The track ISRC."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "TrackInfo":
        """Build Track Information from payload object.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return TrackInfo(
            payload["identifier"],
            payload["isSeekable"],
            payload["author"],
            payload["length"],
            payload["isStream"],
            payload["position"],
            payload["title"],
            payload["sourceName"],
            payload.get("uri", None),
            payload.get("artworkUrl", None),
            payload.get("isrc", None),
        )


@dataclass(order=True, slots=True)
class Track(PayloadObject):
    """Track.

    The base track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track)
    """

    encoded: str
    """The BASE-64 encoded track data."""

    info: TrackInfo
    """Information about the track."""

    plugin_info: typing.Mapping[str, typing.Any]
    """Additional track info provided by plugins."""

    # TODO: Add setter for custom data
    # From: https://github.com/hikari-ongaku/ongaku/commit/6b2e1576626bd2d32072af7e5fadc3c2fd1233dd
    user_data: typing.Mapping[str, typing.Any]
    """Additional track data.

    !!! warning
        If you store a value of any type under the name `ongaku_requestor` it will be overridden.
    """

    requestor: hikari.Snowflake | None
    """The person who requested this track."""

    @classmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> "Track":
        """Build Track from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        user_data: typing.MutableMapping[str, typing.Any] = (
            payload.get("userData") or {}
        )
        requestor = user_data.pop("ongaku_requestor", None)
        return Track(
            payload["encoded"],
            TrackInfo.from_payload(payload["info"]),
            payload["pluginInfo"],
            user_data,
            hikari.Snowflake(requestor) if requestor else None,
        )
