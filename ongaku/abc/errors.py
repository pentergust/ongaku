"""Error ABC's.

The error abstract classes.
"""

import abc
import enum

__all__ = ("ExceptionError", "SeverityType")


class SeverityType(str, enum.Enum):
    """
    Track error severity type.

    The severity type of the lavalink track error.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket#severity)
    """

    COMMON = "common"
    """The cause is known and expected, indicates that there is nothing wrong with the library itself."""
    SUSPICIOUS = "suspicious"
    """The cause might not be exactly known, but is possibly caused by outside factors. For example when an outside service responds in a format that we do not expect."""
    FAULT = "fault"
    """The probable cause is an issue with the library or there is no way to tell what the cause might be. This is the default level and other levels are used in cases where the thrower has more in-depth knowledge about the error."""


class ExceptionError(abc.ABC):
    """
    Exception error.

    The exception error lavalink returns when a track has an exception.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#exception-object)
    """

    @property
    @abc.abstractmethod
    def message(self) -> str | None:
        """The message of the exception."""
        ...

    @property
    @abc.abstractmethod
    def severity(self) -> SeverityType:
        """The severity of the exception."""
        ...

    @property
    @abc.abstractmethod
    def cause(self) -> str:
        """The cause of the exception."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExceptionError):
            return False

        if self.message != other.message:
            return False

        if self.severity != other.severity:
            return False

        return self.cause == other.cause
