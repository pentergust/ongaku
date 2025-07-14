"""Routes.

All the routes for lavalink.
"""

from dataclasses import dataclass
from typing import Final

GET: Final = "GET"
POST: Final = "POST"
PATCH: Final = "PATCH"
DELETE: Final = "DELETE"


@dataclass(frozen=True, slots=True)
class Route:
    """Route.

    The route object that has mostly been built.
    """

    method: str
    path: str
    include_version: bool = True

    def build_url(self, uri: str) -> str:
        """Build the full url."""
        return uri + self.path

    def __str__(self) -> str:
        """Format route as string."""
        return f"{self.method} {self.path}"


# Info

GET_INFO: Final = Route(method=GET, path="/info")
GET_VERSION: Final = Route(method=GET, path="/version", include_version=False)
GET_STATISTICS: Final = Route(method=GET, path="/stats")

# Session

PATCH_SESSION_UPDATE: Final = Route(method=PATCH, path="/sessions/{session_id}")

# Player

GET_PLAYERS: Final = Route(method=GET, path="/sessions/{session_id}/players")

GET_PLAYER: Final = Route(
    method=GET, path="/sessions/{session_id}/players/{guild_id}"
)

PATCH_PLAYER_UPDATE: Final = Route(
    method=PATCH, path="/sessions/{session_id}/players/{guild_id}"
)

DELETE_PLAYER: Final = Route(
    method=DELETE, path="/sessions/{session_id}/players/{guild_id}"
)

# Tracks

GET_LOAD_TRACKS: Final = Route(method=GET, path="/loadtracks")
GET_DECODE_TRACK: Final = Route(method=GET, path="/decodetrack")
POST_DECODE_TRACKS: Final = Route(method=POST, path="/decodetracks")

# Route Planner

GET_ROUTEPLANNER_STATUS: Final = Route(method=GET, path="/routeplanner/status")

POST_ROUTEPLANNER_FREE_ADDRESS: Final = Route(
    POST, "/routeplanner/free/address"
)

POST_ROUTEPLANNER_FREE_ALL: Final = Route(
    method=POST, path="/routeplanner/free/all"
)
