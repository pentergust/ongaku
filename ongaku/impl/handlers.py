"""Handler Impl's.

The handler implemented classes.
"""

import abc
import asyncio
import typing

import hikari

from ongaku import errors
from ongaku.client import Client
from ongaku.impl.session import SessionStatus
from ongaku.player import Player
from ongaku.session import Session

__all__ = ("BaseSessionHandler", "SessionHandler")


class BaseSessionHandler(abc.ABC):
    """
    Session handler base.

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
    def __init__(self, client: Client): ...

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
        """
        Fetch a player.

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
        """
        Delete a player.

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


class SessionHandler(BaseSessionHandler):
    """
    Basic Session Handler.

    This session handler simply fetches the first working session, and returns it.
    If it closes or fails, it switches to the next available one.
    """

    __slots__: typing.Sequence[str] = (
        "_current_session",
        "_players",
        "_sessions",
    )

    def __init__(self, client: Client) -> None:
        self._client = client
        self._is_alive = False
        self._current_session: Session | None = None
        self._sessions: typing.MutableMapping[str, Session] = {}
        self._players: typing.MutableMapping[hikari.Snowflake, Player] = {}

    @property
    def sessions(self) -> typing.Sequence[Session]:
        """The sessions attached to this handler."""
        return tuple(self._sessions.values())

    @property
    def players(self) -> typing.Sequence[Player]:
        """The players attached to this handler."""
        return tuple(self._players.values())

    @property
    def is_alive(self) -> bool:
        """Whether the handler is alive or not."""
        return self._is_alive

    async def start(self) -> None:
        self._is_alive = True

        for _, session in self._sessions.items():
            if session.status == SessionStatus.NOT_CONNECTED:
                await session.start()

    async def stop(self) -> None:
        for session in self.sessions:
            await session.stop()

        self._players.clear()
        self._is_alive = False

    def add_session(self, session: Session) -> Session:
        """Add a session."""
        if self.is_alive:
            asyncio.create_task(session.start())  # noqa: RUF006

        if self._sessions.get(session.name, None) is None:
            self._sessions.update({session.name: session})
            return session

        raise errors.UniqueError(f"The name {session.name} is not unique.")

    def fetch_session(self, name: str | None = None) -> Session:
        if name is not None:
            try:
                return self._sessions[name]
            except KeyError:
                raise errors.SessionMissingError

        if self._current_session:
            return self._current_session

        for session in self.sessions:
            if session.status == SessionStatus.CONNECTED:
                self._current_session = session
                return session

        raise errors.NoSessionsError

    async def delete_session(self, name: str) -> None:
        try:
            session = self._sessions.pop(name)
        except KeyError:
            raise errors.SessionMissingError

        await session.stop()

    def add_player(
        self,
        player: Player,
    ) -> Player:
        if self._players.get(player.guild_id, None) is not None:
            raise errors.UniqueError(
                f"A player with the guild id {player.guild_id} has already been made.",
            )

        self._players.update({player.guild_id: player})

        return player

    def fetch_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> Player:
        player = self._players.get(hikari.Snowflake(guild))

        if player:
            return player

        raise errors.PlayerMissingError

    async def delete_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        try:
            player = self._players.pop(hikari.Snowflake(guild))
        except KeyError:
            raise errors.PlayerMissingError

        await player.disconnect()
