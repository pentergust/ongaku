"""Errors.

All of the ongaku errors.
"""

import abc
import datetime
import enum
import typing

from typing_extensions import Self

from ongaku.impl.payload import PayloadObject

__all__ = (
    "BuildError",
    "ClientAliveError",
    "ClientError",
    "ExceptionError",
    "NoSessionsError",
    "OngakuError",
    "PlayerConnectError",
    "PlayerError",
    "PlayerMissingError",
    "PlayerQueueError",
    "RestEmptyError",
    "RestError",
    "RestExceptionError",
    "RestRequestError",
    "RestStatusError",
    "SessionError",
    "SessionHandlerError",
    "SessionStartError",
    "SeverityType",
    "TimeoutError",
)


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

    @property
    @abc.abstractmethod
    def severity(self) -> SeverityType:
        """The severity of the exception."""

    @property
    @abc.abstractmethod
    def cause(self) -> str:
        """The cause of the exception."""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExceptionError):
            return False

        return (
            self.message == other.message
            and self.severity == other.severity
            and self.cause == other.cause
        )


class OngakuError(Exception):
    """The base ongaku error."""


# Rest:


class RestError(OngakuError):
    """The base rest error for all rest action errors."""


class RestStatusError(RestError):
    """Raised when the status is 4XX or 5XX."""

    __slots__: typing.Sequence[str] = ("_reason", "_status")

    def __init__(self, status: int, reason: str | None) -> None:
        self._status = status
        self._reason = reason

    @property
    def status(self) -> int:
        """The status of the response."""
        return self._status

    @property
    def reason(self) -> str | None:
        """The response of the error."""
        return self._reason


class RestRequestError(RestError, PayloadObject):
    """Raised when a rest error is received from the response."""

    __slots__: typing.Sequence[str] = (
        "_error",
        "_message",
        "_path",
        "_status",
        "_timestamp",
        "_trace",
    )

    def __init__(
        self,
        timestamp: datetime.datetime,
        status: int,
        error: str,
        message: str,
        path: str,
        trace: str | None,
    ) -> None:
        self._timestamp = timestamp
        self._status = status
        self._error = error
        self._message = message
        self._path = path
        self._trace = trace

    @property
    def timestamp(self) -> datetime.datetime:
        """The timestamp of the error in milliseconds since the Unix epoch."""
        return self._timestamp

    @property
    def status(self) -> int:
        """The HTTP status code."""
        return self._status

    @property
    def error(self) -> str:
        """The HTTP status code message."""
        return self._error

    @property
    def message(self) -> str:
        """The error message."""
        return self._message

    @property
    def path(self) -> str:
        """The request path."""
        return self._path

    @property
    def trace(self) -> str | None:
        """The stack trace of the error."""
        return self._trace

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "RestRequestError":
        """Build Rest Request Error from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return RestRequestError(
            datetime.datetime.fromtimestamp(
                int(payload["timestamp"]) / 1000,
                datetime.timezone.utc,
            ),
            payload["status"],
            payload["error"],
            payload["message"],
            payload["path"],
            payload.get("trace", None),
        )


class RestEmptyError(RestError):
    """Raised when the request was 204, but data was requested."""


class RestExceptionError(RestError, ExceptionError, PayloadObject):
    """Raised when a track search results in a error result."""

    __slots__: typing.Sequence[str] = ()

    def __init__(
        self,
        message: str | None,
        severity: SeverityType,
        cause: str,
    ):
        self._message = message
        self._severity = severity
        self._cause = cause

    @classmethod
    def from_error(cls, error: ExceptionError) -> Self:
        return cls(error.message, error.severity, error.cause)

    @property
    def message(self) -> str | None:
        return self._message

    @property
    def severity(self) -> SeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "RestExceptionError":
        """Build Rest Exception Error from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return RestExceptionError(
            payload.get("message", None),
            SeverityType(payload["severity"]),
            payload["cause"],
        )


# Client


class ClientError(OngakuError):
    """The base for all client errors."""


class ClientAliveError(ClientError):
    """Raised when the client is not currently alive, or has crashed."""

    __slots__: typing.Sequence[str] = ("_reason",)

    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        """The reason this error occurred."""
        return self._reason


# Sessions


class SessionError(OngakuError):
    """The base session error for all session related errors."""


class SessionStartError(SessionError):
    """Raised when the session has not started. (has not received the ready payload)."""


class SessionMissingError(SessionError):
    """Raised when the session could not be found."""


# Session Handler


class SessionHandlerError(OngakuError):
    """The base for all session handler related errors."""


class NoSessionsError(SessionHandlerError):
    """Raised when there is no available sessions for the handler to return."""


# Player


class PlayerError(OngakuError):
    """The base for all player related errors."""


class PlayerConnectError(PlayerError):
    """Raised when the player cannot connect to lavalink, or discord."""

    __slots__: typing.Sequence[str] = "_reason"

    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        """The reason for failure of connection."""
        return self._reason


class PlayerQueueError(PlayerError):
    """Raised when the players queue is empty."""

    __slots__: typing.Sequence[str] = "_reason"

    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        """Reason for the queue error."""
        return self._reason


class PlayerMissingError(PlayerError):
    """Raised when the player could not be found."""


# Others:


class BuildError(OngakuError):
    """Raised when a abstract class fails to build."""

    __slots__: typing.Sequence[str] = ("_exception", "_reason")

    def __init__(
        self, exception: Exception | None, reason: str | None = None
    ) -> None:
        self._exception = exception
        self._reason = reason

    @property
    def exception(self) -> Exception | None:
        """The exception raised to receive the build error."""
        return self._exception

    @property
    def reason(self) -> str | None:
        """The reason this error occurred."""
        return self._reason


class TimeoutError(OngakuError):
    """Raised when an event times out."""


class UniqueError(OngakuError):
    """Raised when a value should be unique, but is not."""

    __slots__: typing.Sequence[str] = "_reason"

    def __init__(self, reason: str | None) -> None:
        self._reason = reason

    @property
    def reason(self) -> str | None:
        """The reason for the unique error."""
        return self._reason
