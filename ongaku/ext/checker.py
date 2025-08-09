"""Allows for you to check if a string is a link or a query."""

import urllib.parse as urlparse

__all__ = ("check",)

_YOUTUBE_URLS = (
    "www.youtube.com",
    "youtube.com",
    "www.youtu.be",
    "youtu.be",
    "music.youtube.com",
)


async def check(query: str, /) -> bool:
    """Check a string.

    Allows for the user to check a current string, and see what type it is.

    !!! warning
        Currently the checker only supports youtube url's.

    Example
    -------
    ```py
    from ongaku.ext import checker

    if checker.check(query):
        print("This is a video/playlist")
    else:
        print("This is a query")
    ```

    Parameters
    ----------
    query : str
        The query you wish to check.

    Returns
        bool
        If True, then it is a video/playlist, otherwise its just a query.
    """
    url = urlparse.urlparse(query)
    queries: dict[str, str] = {}
    if url.query.strip() != "":
        url_queries = url.query.split("&")
        for url_query in url_queries:
            url_query_split = url_query.split("=")
            queries[url_query_split[0]] = url_query_split[1]

    return url.netloc in _YOUTUBE_URLS
