"""Handler Abc's.

The handler abstract class.
"""

from __future__ import annotations

import abc
import typing

import hikari

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.player import Player
    from ongaku.session import Session


class BaseSessionHandler(abc.ABC):
    """Session handler base.

    The base session handler object.

    !!! note
        All custom session handlers **must** subclass this.

    Parameters
    ----------
    client
        The base ongaku client.
    """

    __slots__ = ("_client", "_is_alive")
    _is_alive: bool

    @abc.abstractmethod
    def __init__(self, client: "Client"): ...

    @property
    @abc.abstractmethod
    def sessions(self) -> typing.Sequence[Session]:
        """The sessions attached to this handler."""

    @property
    @abc.abstractmethod
    def players(self) -> typing.Sequence[Player]:
        """The players attached to this handler."""

    @property
    def is_alive(self) -> bool:
        """Whether the handler is alive or not."""
        return self._is_alive

    @abc.abstractmethod
    async def start(self) -> None:
        """Start the session handler.

        Starts up the session handler and attempts to connect all sessions to their websocket.
        """

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the session handler.

        Stops the session handler and kills all players and sessions.
        """

    @abc.abstractmethod
    def add_session(self, session: Session) -> Session:
        """Add a session.

        Add a new session to the session handler.

        Parameters
        ----------
        session
            The session to add to the session handler.

        Returns
        -------
        Session
            The session that was added to the handler.
        """

    @abc.abstractmethod
    def fetch_session(self, name: str | None = None) -> Session:
        """Fetch a session.

        Returns a valid session.

        !!! note
            If a name is provided, only that session will be attempted to be returned.

        Parameters
        ----------
        name
            The name of the session.

        Returns
        -------
        Session
            The session to use.

        Raises
        ------
        NoSessionError
            Raised when there is no available sessions for the handler to return.
        SessionMissingError
            Raised when a session is requested, but does not exist.
        """

    @abc.abstractmethod
    async def delete_session(self, name: str) -> None:
        """Delete a session.

        Delete a session from the session handler.

        Parameters
        ----------
        name
            The name of the session to delete.

        Returns
        -------
        Session
            The session that was added to the handler.

        Raises
        ------
        SessionMissingError
            Raised when the session does not exist.
        """

    @abc.abstractmethod
    def add_player(self, player: Player) -> Player:
        """Add a player.

        Add a new player to the session handler.

        Parameters
        ----------
        player
            The player to add to the session handler.

        Returns
        -------
        Player
            The player you added to the session handler.
        """

    @abc.abstractmethod
    def fetch_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> Player:
        """Fetch a player.

        Fetches an existing player.

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to fetch the player for.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """

    @abc.abstractmethod
    async def delete_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        """Delete a player.

        Delete a pre-existing player.

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to delete the player from.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """
