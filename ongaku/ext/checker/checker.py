"""Checker.

The extension, that allows you to check if a link is a url, or a video/playlist!
"""

import urllib.parse as urlparse

from .abc import Checked
from .abc import CheckedType


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

    if url.netloc in [
        "www.youtube.com",
        "youtube.com",
        "www.youtu.be",
        "youtu.be",
        "music.youtube.com",
    ]:
        if url.path == "/playlist":
            return Checked(queries["list"], CheckedType.PLAYLIST)
        if url.path == "/watch":
            return Checked(queries["v"], CheckedType.TRACK)

    return Checked(query, CheckedType.QUERY)
