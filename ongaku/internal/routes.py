"""Routes.

All the routes for lavalink.
"""

from __future__ import annotations

import typing

GET: typing.Final[str] = "GET"
POST: typing.Final[str] = "POST"
PATCH: typing.Final[str] = "PATCH"
DELETE: typing.Final[str] = "DELETE"


class Route:
    """Route.

    The route object that has mostly been built.
    """

    def __init__(
        self, method: str, path: str, *, include_version: bool = True
    ) -> None:
        self._method = method
        self._path = path
        self._include_version = include_version

    @property
    def method(self) -> str:
        """The route method."""
        return self._method

    @property
    def path(self) -> str:
        """The path."""
        return self._path

    @property
    def include_version(self) -> bool:
        """Whether to include the version."""
        return self._include_version

    def build_url(self, uri: str) -> str:
        """Build the full url."""
        return uri + self.path

    def __str__(self) -> str:
        """."""
        return f"{self.method} {self.path}"


# Info

GET_INFO: typing.Final[Route] = Route(GET, "/info")
GET_VERSION: typing.Final[Route] = Route(GET, "/version", include_version=False)
GET_STATISTICS: typing.Final[Route] = Route(GET, "/stats")

# Session

PATCH_SESSION_UPDATE: typing.Final[Route] = Route(
    PATCH, "/sessions/{session_id}"
)

# Player

GET_PLAYERS: typing.Final[Route] = Route(GET, "/sessions/{session_id}/players")

GET_PLAYER: typing.Final[Route] = Route(
    GET,
    "/sessions/{session_id}/players/{guild_id}",
)

PATCH_PLAYER_UPDATE: typing.Final[Route] = Route(
    PATCH,
    "/sessions/{session_id}/players/{guild_id}",
)

DELETE_PLAYER: typing.Final[Route] = Route(
    DELETE,
    "/sessions/{session_id}/players/{guild_id}",
)

# Tracks

GET_LOAD_TRACKS: typing.Final[Route] = Route(GET, "/loadtracks")
GET_DECODE_TRACK: typing.Final[Route] = Route(GET, "/decodetrack")
POST_DECODE_TRACKS: typing.Final[Route] = Route(POST, "/decodetracks")

# Route Planner

GET_ROUTEPLANNER_STATUS: typing.Final[Route] = Route(
    GET, "/routeplanner/status"
)

POST_ROUTEPLANNER_FREE_ADDRESS: typing.Final[Route] = Route(
    POST,
    "/routeplanner/free/address",
)

POST_ROUTEPLANNER_FREE_ALL: typing.Final[Route] = Route(
    POST, "/routeplanner/free/all"
)
