"""Youtube.

Endpoints for the youtube source plugin.
"""

from __future__ import annotations

from ongaku.ext.youtube.endpoints import fetch_youtube
from ongaku.ext.youtube.endpoints import update_youtube

__all__ = ("fetch_youtube", "update_youtube")
