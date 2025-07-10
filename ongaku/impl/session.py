"""Session Impl's.

The session implemented classes.

TODO: maybe rename base session to BaseSession
"""

from ongaku.abc import session as session_

__all__ = ("Session",)


class Session(session_.Session):
    def __init__(self, resuming: bool, timeout: int) -> None:
        self._resuming = resuming
        self._timeout = timeout
