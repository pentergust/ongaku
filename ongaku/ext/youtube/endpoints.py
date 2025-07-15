from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ongaku.session import Session

__all__ = ("fetch_youtube", "update_youtube")


async def fetch_youtube(session: Session) -> str | None:
    """Gets the current Youtube Refresh Token.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://github.com/lavalink-devs/youtube-source?tab=readme-ov-file#get-youtube)

    Example
    -------
    ```py
    token = await client.rest.fetch_youtube()

    print(token)
    ```

    Parameters
    ----------
    session
        If provided, the session to use for this request.

    Raises
    ------
    NoSessionsError
        Raised when there is no available sessions for this request to take place.
    TimeoutError
        Raised when the request takes too long to respond.
    RestEmptyError
        Raised when the request required a return type, but received nothing, or a 204 response.
    RestStatusError
        Raised when a 4XX or a 5XX status is received.
    BuildError
        Raised when the statistics could not be built.
    RestRequestError
        Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
    RestError
        Raised when an unknown error is caught.

    Returns
    -------
    str
        The refresh token.
    None
        Returned when youtube is disabled.
    """
    response = await session.request("GET", "/youtube", str)

    if response is None:
        raise ValueError("Response is required for this request.")

    return response


async def update_youtube(
    session: Session,
    /,
    *,
    refresh_token: str | None = None,
    skip_initialization: bool | None = None,
    po_token: str | None = None,
    visitor_data: str | None = None,
) -> None:
    """Update youtube endpoints.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://github.com/lavalink-devs/youtube-source?tab=readme-ov-file#post-youtube)

    Example
    -------
    ```py
    await client.rest.update_youtube(
        refresh_token="acooltoken",
        skip_initialization=True,
        po_token="anothercooltoken",
        visitor_data="visitordata",
    )
    ```

    Parameters
    ----------
    refresh_token
        The refresh token to use.
    skip_initialization
        Whether to skip initialization of OAuth.
    po_token
        The PO Token to use.
    visitor_data
        The visitor data to use.
    session
        If provided, the session to use for this request.

    Raises
    ------
    ValueError
        Raised when no values have been modified.
    NoSessionsError
        Raised when there is no available sessions for this request to take place.
    TimeoutError
        Raised when the request takes too long to respond.
    RestStatusError
        Raised when a 4XX or a 5XX status is received.
    RestRequestError
        Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
    RestError
        Raised when an unknown error is caught.
    """
    if (
        not refresh_token
        and not skip_initialization
        and not po_token
        and not visitor_data
    ):
        raise ValueError("At least one value must be modified.")

    json: dict[str, typing.Any] = {}

    if not refresh_token:
        json["refreshToken"] = refresh_token

    if not skip_initialization:
        json["skipInitialization"] = skip_initialization

    if not po_token:
        json["poToken"] = po_token

    if not visitor_data:
        json["visitorData"] = visitor_data

    await session.request("POST", "/youtube", None, json=json)
