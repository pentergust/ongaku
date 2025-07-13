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

GET_INFO: Final = Route(GET, "/info")
GET_VERSION: Final = Route(GET, "/version", include_version=False)
GET_STATISTICS: Final = Route(GET, "/stats")

# Session

PATCH_SESSION_UPDATE: Final = Route(PATCH, "/sessions/{session_id}")

# Player

GET_PLAYERS: Final = Route(GET, "/sessions/{session_id}/players")

GET_PLAYER: Final = Route(GET, "/sessions/{session_id}/players/{guild_id}")

PATCH_PLAYER_UPDATE: Final = Route(
    PATCH, "/sessions/{session_id}/players/{guild_id}"
)

DELETE_PLAYER: Final = Route(
    DELETE, "/sessions/{session_id}/players/{guild_id}"
)

# Tracks

GET_LOAD_TRACKS: Final = Route(GET, "/loadtracks")
GET_DECODE_TRACK: Final = Route(GET, "/decodetrack")
POST_DECODE_TRACKS: Final = Route(POST, "/decodetracks")

# Route Planner

GET_ROUTEPLANNER_STATUS: Final = Route(GET, "/routeplanner/status")

POST_ROUTEPLANNER_FREE_ADDRESS: Final = Route(
    POST, "/routeplanner/free/address"
)

POST_ROUTEPLANNER_FREE_ALL: Final = Route(POST, "/routeplanner/free/all")
