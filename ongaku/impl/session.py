"""Session Impl's.

The session implemented classes.

TODO: maybe rename base session to BaseSession
"""

import typing

from ongaku.abc import session as session_

__all__ = ("Session",)


class Session(session_.Session):
    def __init__(self, resuming: bool, timeout: int) -> None:
        self._resuming = resuming
        self._timeout = timeout

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Session":
        """Build Session from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Session(payload["resuming"], payload["timeout"])
