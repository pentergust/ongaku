"""Handler impl`s.

Basic event handler implementation.
"""

from __future__ import annotations

import asyncio
import typing

import hikari

from ongaku import errors
from ongaku.handler.abc import BaseSessionHandler
from ongaku.impl.session import SessionStatus

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.player import Player
    from ongaku.session import Session


class SessionHandler(BaseSessionHandler):
    """Basic Session Handler.

    This session handler simply fetches the first working session, and returns it.
    If it closes or fails, it switches to the next available one.
    """

    __slots__ = ("_current_session", "_players", "_sessions")

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

    # Manage sessions
    # ===============

    def add_session(self, session: Session) -> Session:
        if self._sessions.get(session.name) is not None:
            raise errors.UniqueError(f"The name {session.name} is not unique.")

        if not self.is_alive:
            asyncio.create_task(session.start())  # noqa: RUF006

        self._sessions[session.name] = session
        return session

    def fetch_session(self, name: str | None = None) -> Session:
        if name is not None:
            try:
                return self._sessions[name]
            except KeyError as e:
                raise errors.SessionMissingError from e

        if self._current_session is not None:
            return self._current_session

        for session in self.sessions:
            if session.status == SessionStatus.CONNECTED:
                self._current_session = session
                return session

        raise errors.NoSessionsError

    async def delete_session(self, name: str) -> None:
        try:
            session = self._sessions.pop(name)
        except KeyError as e:
            raise errors.SessionMissingError from e

        await session.stop()

    # Manage players
    # ==============

    def add_player(self, player: Player) -> Player:
        if self._players.get(player.guild_id, None) is not None:
            raise errors.UniqueError(
                f"A player with the guild id {player.guild_id} has already been made.",
            )
        self._players[player.guild_id] = player
        return player

    def fetch_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> Player:
        player = self._players.get(hikari.Snowflake(guild))
        if player is not None:
            return player

        raise errors.PlayerMissingError(f"No player found for {guild}")

    async def delete_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        try:
            player = self._players.pop(hikari.Snowflake(guild))
        except KeyError as e:
            raise errors.PlayerMissingError from e

        await player.disconnect()
