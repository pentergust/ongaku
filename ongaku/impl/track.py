"""Track Impl's.

The track implemented classes.
"""

import typing

if typing.TYPE_CHECKING:
    import hikari

from ongaku.abc import track as track_

__all__ = ("Track", "TrackInfo")


class TrackInfo(track_.TrackInfo):
    def __init__(
        self,
        identifier: str,
        is_seekable: bool,
        author: str,
        length: int,
        is_stream: bool,
        position: int,
        title: str,
        source_name: str,
        uri: str | None,
        artwork_url: str | None,
        isrc: str | None,
    ) -> None:
        self._identifier = identifier
        self._is_seekable = is_seekable
        self._author = author
        self._length = length
        self._is_stream = is_stream
        self._position = position
        self._title = title
        self._source_name = source_name
        self._uri = uri
        self._artwork_url = artwork_url
        self._isrc = isrc

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


class Track(track_.Track):
    def __init__(
        self,
        encoded: str,
        info: track_.TrackInfo,
        plugin_info: typing.Mapping[str, typing.Any],
        user_data: typing.Mapping[str, typing.Any],
        requestor: hikari.Snowflake | None,
    ) -> None:
        self._encoded = encoded
        self._info = info
        self._plugin_info = plugin_info
        self._user_data = user_data
        self._requestor = requestor

    @classmethod
    def build_track(cls, payload: typing.Mapping[str, typing.Any]) -> "Track":
        """Build Track from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        user_data: typing.MutableMapping[str, typing.Any] = (
            payload["userData"] if payload.get("userData", None) else {}
        )
        requestor = user_data.pop("ongaku_requestor", None)
        return Track(
            payload["encoded"],
            TrackInfo.from_payload(payload["info"]),
            payload["pluginInfo"],
            user_data,
            hikari.Snowflake(requestor) if requestor else None,
        )
