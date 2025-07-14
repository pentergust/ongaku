"""Client.

The base client for ongaku.
"""

from __future__ import annotations

import typing

import aiohttp
import hikari
from loguru import logger
from typing_extensions import Self

from ongaku import errors
from ongaku.handler.abc import BaseSessionHandler
from ongaku.handler.base import SessionHandler
from ongaku.player import Player
from ongaku.rest import RESTClient
from ongaku.session import Session

if typing.TYPE_CHECKING:
    import arc
    import tanjun


__all__ = ("Client",)


class Client:
    """The client for ongaku.

    Example
    -------
    ```py
    bot = hikari.GatewayBot("...")
    client = ongaku.Client(bot)
    ```

    Parameters
    ----------
    app
        The application that the client will attach too.
    session_handler
        The session handler to use for the current client.
    attempts
        The amount of attempts a session will try to connect to the server.
    """

    __slots__ = (
        "_app",
        "_attempts",
        "_client_session",
        "_is_alive",
        "_rest_client",
        "_session_handler",
    )

    def __init__(
        self,
        app: hikari.GatewayBotAware,
        *,
        session_handler: type[BaseSessionHandler] = SessionHandler,
        attempts: int = 3,
    ) -> None:
        self._attempts = attempts
        self._app = app
        self._client_session: aiohttp.ClientSession | None = None

        self._rest_client = RESTClient(self)
        self._is_alive = False
        self._session_handler = session_handler(self)

        app.event_manager.subscribe(hikari.StartedEvent, self._start_event)
        app.event_manager.subscribe(hikari.StoppingEvent, self._stop_event)

    @classmethod
    def from_arc(
        cls,
        client: arc.GatewayClient,
        *,
        session_handler: type[BaseSessionHandler] = SessionHandler,
        attempts: int = 3,
    ) -> Self:
        """From Arc.

        This supports `client` and `player` [injection](../gs/injection.md) for [Arc](https://github.com/hypergonial/hikari-arc)

        Example
        -------
        ```py
        bot = arc.GatewayBot(...)
        client = arc.GatewayClient(bot)
        ongaku_client = ongaku.Client.from_arc(client)
        ```

        Parameters
        ----------
        client
            Your Gateway client for arc.
        session_handler
            The session handler to use for the current client.
        attempts
            The amount of attempts a session will try to connect to the server.
        """
        instance = cls(
            client.app, session_handler=session_handler, attempts=attempts
        )

        client.set_type_dependency(Client, instance)
        client.add_injection_hook(instance._arc_player_injector)
        return instance

    @classmethod
    def from_tanjun(
        cls,
        client: tanjun.abc.Client,
        *,
        session_handler: type[BaseSessionHandler] = SessionHandler,
        attempts: int = 3,
    ) -> Self:
        """From Tanjun.

        This supports `client` [injection](../gs/injection.md) for [Tanjun](https://github.com/FasterSpeeding/Tanjun)

        Example
        -------
        ```py
        bot = arc.GatewayBot(...)
        client = tanjun.Client.from_gateway_bot(bot)
        ongaku_client = ongaku.Client.from_tanjun(client)
        ```

        Parameters
        ----------
        client
            Your Gateway client from tanjun.
        session_handler
            The session handler to use for the current client.
        attempts
            The amount of attempts a session will try to connect to the server.
        """
        try:
            app = client.get_type_dependency(hikari.GatewayBotAware)
        except KeyError:
            raise Exception("The gateway bot requested was not found.")

        instance = cls(app, session_handler=session_handler, attempts=attempts)
        client.set_type_dependency(Client, instance)
        return instance

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The application this client is included in."""
        return self._app

    @property
    def rest(self) -> RESTClient:
        """The rest client for calling rest actions."""
        return self._rest_client

    @property
    def is_alive(self) -> bool:
        """
        Whether the session handler is alive.

        !!! note
            If the `hikari.StartedEvent` has occurred, and this is False, ongaku is no longer running and has crashed. Check your logs.
        """
        return self.session_handler.is_alive

    @property
    def session_handler(self) -> BaseSessionHandler:
        """Session handler.

        The session handler that is currently controlling the sessions.

        !!! warning
            This should not be touched, or used if you do not know what you are doing.
            Please use the other methods in client for anything session handler related.
        """
        return self._session_handler

    def _get_client_session(self) -> aiohttp.ClientSession:
        if self._client_session is None or self._client_session.closed:
            self._client_session = aiohttp.ClientSession()

        return self._client_session

    async def _start_event(self, event: hikari.StartedEvent) -> None:
        logger.debug("Starting up ongaku.")
        await self.session_handler.start()

    async def _stop_event(self, event: hikari.StoppingEvent) -> None:
        logger.debug("Shutting down ongaku.")
        await self.session_handler.stop()

        if self._client_session is not None and not self._client_session.closed:
            await self._client_session.close()

    async def _arc_player_injector(
        self, ctx: arc.GatewayContext, inj_ctx: arc.InjectorOverridingContext
    ) -> None:
        logger.debug("Attempting to inject player.")

        if ctx.guild_id is None:
            logger.debug("Player ignored, not in guild.")
            return

        try:
            player = self.fetch_player(ctx.guild_id)
        except errors.PlayerMissingError:
            logger.debug("Player not found for context.")
            return

        inj_ctx.set_type_dependency(Player, player)

    def create_session(
        self,
        name: str,
        ssl: bool = False,
        host: str = "127.0.0.1",
        port: int = 2333,
        password: str = "youshallnotpass",
    ) -> Session:
        """Create a new session for the session handler.

        Example
        -------
        ```py
        client = ongaku.Client(...)

        client.add_session(host="192.168.68.69")
        ```

        !!! warning
            The name set must be unique, otherwise an error will be raised.

        Parameters
        ----------
        name
            The name of the session
        ssl
            Whether the server uses `https` or just `http`.
        host
            The host of the lavalink server.
        port
            The port of the lavalink server.
        password
            The password of the lavalink server.

        Returns
        -------
        Session
            The session that was added to the handler.

        Raises
        ------
        UniqueError
        """
        return self.session_handler.add_session(
            Session(self, name, ssl, host, port, password, self._attempts)
        )

    def fetch_session(self, name: str) -> Session:
        """Fetch a session from the session handler.

        Parameters
        ----------
        name
            The name of the session

        Returns
        -------
        Session
            The session that was requested.

        Raises
        ------
        SessionMissingError
            Raised when the session does not exist.
        """
        return self.session_handler.fetch_session(name)

    async def delete_session(self, name: str) -> None:
        """Delete a session from the session handler.

        Parameters
        ----------
        name
            The name of the session

        Raises
        ------
        SessionMissingError
            Raised when the session does not exist.
        """
        await self.session_handler.delete_session(name)

    def create_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> Player:
        """Create a new player to play songs on.

        Tries to get an existing player before creating a new one.

        Example
        -------
        ```py
        client = ongaku.Client(...)
        player = await client.create_player(guild_id)
        await player.connect(channel_id)
        await player.play(track)
        ```

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to create a player for.

        Returns
        -------
        Player
            The player that was created.

        Raises
        ------
        NoSessionsError
            When there is no available sessions.
        """
        try:
            return self.fetch_player(hikari.Snowflake(guild))
        except errors.PlayerMissingError:
            pass

        session = self.session_handler.fetch_session()
        new_player = Player(session, hikari.Snowflake(guild))
        return self.session_handler.add_player(new_player)

    def fetch_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> Player:
        """Fetches an existing player.

        Example
        -------
        ```py
        client = ongaku.Client(...)
        player = await client.fetch_player(guild_id)

        await player.pause()
        ```

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to fetch the player for.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """
        return self.session_handler.fetch_player(guild)

    async def delete_player(
        self, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        """Delete a pre-existing player.

        Example
        -------
        ```py
        client = ongaku.Client(...)
        await client.delete_player(...)
        ```

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to delete the player from.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """
        await self.session_handler.delete_player(guild)
