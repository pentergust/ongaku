"""Allows for you to check if a string is a link or a query."""

import urllib.parse as urlparse
from dataclasses import dataclass
from enum import IntEnum

__all__ = ("Checked", "CheckedType", "check")

_YOUTUBE_URLS = (
    "www.youtube.com",
    "youtube.com",
    "www.youtu.be",
    "youtu.be",
    "music.youtube.com",
)


class CheckedType(IntEnum):
    """The type of result you have received."""

    QUERY = 0
    """The result was a query."""
    TRACK = 1
    """The result was a track."""
    PLAYLIST = 2
    """The result was a playlist."""


@dataclass(slots=True, frozen=True)
class Checked:
    """The checked, and confirmed value, with its specific type attached."""

    value: str
    """The value.

    This is the value, based on the [type][ongaku.ext.checker.abc.CheckedType] it is.
    """

    type: CheckedType
    """The type of the checked value."""


async def check(query: str) -> Checked:
    """Check a string.

    Allows for the user to check a current string, and see what type it is.

    !!! warning
        Currently the checker only supports youtube url's.

    Example
    -------
    ```py
    from ongaku.ext import checker

    response = checker.check(query)

    if checked_query.type == checker.CheckedType.QUERY:
        print(f"Query: {checked_query.value}")
    else:
        print(f"Link: {checked_query.value}")
    ```

    Parameters
    ----------
    query : str
        The query you wish to check.
    """
    url = urlparse.urlparse(query)
    queries: dict[str, str] = {}

    if url.query.strip() != "":
        url_queries = url.query.split("&")
        for url_query in url_queries:
            url_query_split = url_query.split("=")
            queries[url_query_split[0]] = url_query_split[1]

    if url.netloc in _YOUTUBE_URLS:
        if url.path == "/playlist":
            return Checked(queries["list"], CheckedType.PLAYLIST)
        if url.path == "/watch":
            return Checked(queries["v"], CheckedType.TRACK)

    return Checked(query, CheckedType.QUERY)
