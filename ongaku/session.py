"""Session.

Session related objects.
"""

from __future__ import annotations

import asyncio
import typing

import aiohttp
import hikari
import orjson
from loguru import logger

from ongaku import errors, events
from ongaku.__metadata__ import __version__
from ongaku.impl.player import State
from ongaku.impl.session import SessionStatus, WebsocketEvent, WebsocketOPCode
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.handler.abc import BaseSessionHandler
    from ongaku.player import Player


RequestT = typing.TypeVar(
    "RequestT",
    str,
    int,
    bool,
    float,
    dict[str, typing.Any],
    list[typing.Any],
    tuple[typing.Any, ...],
)
"""Request Type.

The types you can request for.
"""


RequestorT: typing.TypeAlias = (
    hikari.SnowflakeishOr[hikari.User] | hikari.SnowflakeishOr[hikari.Member]
)
"""Requestor Type.

The types to set for a requestor of a track.s
"""

__all__ = ("Session",)


class Session:
    """The base session object.

    Parameters
    ----------
    client
        The ongaku client attached to this session.
    name
        The name of the session.
    ssl
        Whether the server is `https` or just `http`.
    host
        The host of the lavalink server.
    port
        The port of the lavalink server.
    password
        The password of the lavalink server.
    attempts
        The attempts that the session is allowed to use, before completely shutting down.
    """

    __slots__: typing.Sequence[str] = (
        "_attempts",
        "_authorization_headers",
        "_base_uri",
        "_client",
        "_host",
        "_name",
        "_password",
        "_players",
        "_port",
        "_remaining_attempts",
        "_session_id",
        "_session_task",
        "_ssl",
        "_status",
        "_websocket_headers",
    )

    def __init__(
        self,
        client: Client,
        name: str,
        ssl: bool,
        host: str,
        port: int,
        password: str,
        attempts: int,
    ) -> None:
        self._client = client
        self._name = name
        self._ssl = ssl
        self._host = host
        self._port = port
        self._password = password
        self._attempts = attempts
        self._remaining_attempts = attempts
        self._base_uri = f"http{'s' if ssl else ''}://{host}:{port}"
        self._session_id: str | None = None
        self._session_task: asyncio.Task[None] | None = None
        self._status = SessionStatus.NOT_CONNECTED
        self._players: typing.MutableMapping[hikari.Snowflake, Player] = {}
        self._websocket_headers: typing.MutableMapping[str, typing.Any] = {}
        self._authorization_headers: typing.Mapping[str, typing.Any] = {
            "Authorization": password,
        }

    @property
    def client(self) -> Client:
        """The client this session is included in."""
        return self._client

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The application this session is included in."""
        return self.client.app

    @property
    def name(self) -> str:
        """The name of the session."""
        return self._name

    @property
    def ssl(self) -> bool:
        """Whether the server uses `https` or just `http`."""
        return self._ssl

    @property
    def host(self) -> str:
        """The host or domain of the site."""
        return self._host

    @property
    def port(self) -> int:
        """The port of the server."""
        return self._port

    @property
    def password(self) -> str:
        """The password for the server."""
        return self._password

    @property
    def base_uri(self) -> str:
        """The base URI for the server."""
        return self._base_uri

    @property
    def auth_headers(self) -> typing.Mapping[str, typing.Any]:
        """The headers required for authorization."""
        return self._authorization_headers

    @property
    def status(self) -> SessionStatus:
        """The current status of the session."""
        return self._status

    @property
    def session_id(self) -> str | None:
        """The current session id.

        !!! note
            Shows up as none if the current session failed to connect, or has not connected yet.
        """
        return self._session_id

    # TODO: Split requestor and validator
    async def request(
        self,
        method: str,
        path: str,
        return_type: type[RequestT] | None,
        *,
        headers: typing.Mapping[str, typing.Any] = {},
        json: typing.Mapping[str, typing.Any]
        | typing.Sequence[typing.Any] = {},
        params: typing.Mapping[str, typing.Any] = {},
        ignore_default_headers: bool = False,
        version: bool = True,
    ) -> RequestT | None:
        """Make a http(s) request to the current session.

        Parameters
        ----------
        method
            The method to send the request as. `GET`, `POST`, `PATCH`, `DELETE`, `PUT`
        path
            The path to the url. e.g. `/v4/info`
        return_type
            The response type you expect.
        headers
            The headers to send.
        json
            The json data to send.
        params
            The parameters to send.
        ignore_default_headers
            Whether to ignore the default headers or not.
        version
            Whether or not to include the version in the path.

        Returns
        -------
        types.RequestT | None
            Your requested type of data.

        Raises
        ------
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the mapping or sequence could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        session = self.client._get_client_session()
        new_headers: typing.MutableMapping[str, typing.Any] = dict(headers)

        if ignore_default_headers is False:
            new_headers.update(self.auth_headers)

        new_params: typing.MutableMapping[str, typing.Any] = dict(params)
        logger.trace(
            "Making request to {}{}{} with headers: {} and json: {} and params: {}",
            self.base_uri,
            "/v4" if version else "",
            path,
            new_headers,
            json,
            new_params,
        )

        response = await session.request(
            method,
            f"{self.base_uri}{'/v4' if version else ''}{path}",
            headers=new_headers,
            json=json,
            params=new_params,
        )

        if response.status == 204 and return_type is not None:
            raise errors.RestEmptyError(f"Excepted {return_type} got None")

        if response.status >= 400:
            payload = await response.text()
            if len(payload) == 0:
                raise errors.RestStatusError(response.status, response.reason)

            try:
                rest_error = errors.RestRequestError.from_payload(payload)
            except Exception as e:
                raise errors.RestStatusError(
                    response.status, response.reason
                ) from e
            raise rest_error

        if return_type is None:
            return None

        payload = await response.text()

        if issubclass(return_type, str | int | bool | float):
            return return_type(payload)

        try:
            json_payload = orjson.loads(payload)
        except Exception as e:
            raise errors.BuildError(e, response.reason) from e

        return return_type(json_payload)

    # TODO: Refactor this code
    def _handle_event(
        self, event: WebsocketEvent, payload: dict[str, typing.Any]
    ) -> events.OngakuEvent:
        if event == WebsocketEvent.TRACK_START_EVENT:
            return events.TrackStartEvent(
                self.client,
                self,
                hikari.Snowflake(payload["guildId"]),
                Track.from_payload(payload["track"]),
            )

        elif event == WebsocketEvent.TRACK_END_EVENT:
            return events.TrackEndEvent(
                self.client,
                self,
                hikari.Snowflake(payload["guildId"]),
                Track.from_payload(payload["track"]),
                events.TrackEndReasonType(payload["reason"]),
            )

        elif event == WebsocketEvent.TRACK_EXCEPTION_EVENT:
            return events.TrackExceptionEvent(
                self.client,
                self,
                hikari.Snowflake(payload["guildId"]),
                Track.from_payload(payload["track"]),
                events.TrackExceptionError.from_payload(payload["exception"]),
            )

        elif event == WebsocketEvent.TRACK_STUCK_EVENT:
            return events.TrackStuckEvent(
                self.client,
                self,
                hikari.Snowflake(payload["guildId"]),
                Track.from_payload(payload["track"]),
                payload["thresholdMs"],
            )
        return events.WebsocketClosedEvent(
            self.client,
            self,
            hikari.Snowflake(payload["guildId"]),
            payload["code"],
            payload["reason"],
            payload["byRemote"],
        )

    def _handle_op_code(self, data: str) -> events.OngakuEvent:
        payload = orjson.loads(data)
        if isinstance(payload, typing.Sequence):
            raise errors.BuildError(
                None,
                "Invalid data received. Must be of type 'typing.Mapping' and not 'typing.Sequence'",
            )

        op_code = WebsocketOPCode(payload["op"])
        if op_code == WebsocketOPCode.READY:
            event = events.ReadyEvent(
                self.client, self, payload["resumed"], payload["sessionId"]
            )
            self._session_id = event.session_id
            return event

        elif op_code == WebsocketOPCode.PLAYER_UPDATE:
            return events.PlayerUpdateEvent(
                self.client,
                self,
                hikari.Snowflake(payload["guildId"]),
                State.from_payload(payload["state"]),
            )

        elif op_code == WebsocketOPCode.STATS:
            stats = Statistics.from_payload(payload)
            return events.StatisticsEvent(
                self.client,
                self,
                stats.players,
                stats.playing_players,
                stats.uptime,
                stats.memory,
                stats.cpu,
                stats.frame_stats,
            )

        event_type = WebsocketEvent(payload["type"])
        return self._handle_event(event_type, payload)

    def _handle_ws_message(self, msg: aiohttp.WSMessage) -> bool:
        """Returns false if failure or closure, true otherwise."""
        if msg.type == aiohttp.WSMsgType.TEXT:
            payload_event = events.PayloadEvent(self.client, self, msg.data)
            event = self._handle_op_code(msg.data)
            self.app.event_manager.dispatch(payload_event, return_tasks=False)
            self.app.event_manager.dispatch(event, return_tasks=False)
            return True

        if msg.type == aiohttp.WSMsgType.ERROR:
            logger.warning("An error occurred. {}", msg.data)

        elif msg.type == aiohttp.WSMsgType.CLOSED:
            logger.warning("Told to close. [{}]:{}", msg.data.name, msg.extra)

        return False

    def _get_bot(self) -> hikari.OwnUser:
        bot = self.app.get_me()
        if bot is None:
            logger.warning("Fetching the bot failed as it does not exist.")
            if self._remaining_attempts > 0:
                self._status = SessionStatus.NOT_CONNECTED
            else:
                self._status = SessionStatus.FAILURE
            raise errors.SessionStartError
        return bot

    async def _websocket(self) -> None:
        logger.trace("Start websocket connection to session {}", self.name)
        bot = self._get_bot()
        self._websocket_headers = {
            "User-Id": str(int(bot.id)),
            "Client-Name": f"{bot.global_name or 'unknown'}/{__version__}",
        }
        new_headers = dict(self._websocket_headers)
        new_headers.update(self.auth_headers)

        while self._remaining_attempts >= 1:
            if self._remaining_attempts != self._attempts:
                await asyncio.sleep(2.5)

            self._remaining_attempts -= 1
            try:
                session = self.client._get_client_session()
                async with session.ws_connect(
                    self.base_uri + "/v4/websocket",
                    headers=new_headers,
                    autoclose=False,
                ) as ws:
                    logger.trace("Connected to session {}", self.name)
                    self._status = SessionStatus.CONNECTED
                    async for msg in ws:
                        if not self._handle_ws_message(msg):
                            self._status = SessionStatus.FAILURE
                            await self.transfer(self.client.session_handler)
                            return
            except Exception as e:
                logger.exception(e)
                logger.warning("Websocket connection failure: {}", e)
                self._status = SessionStatus.NOT_CONNECTED
                break

        logger.warning("Session {} has no more attempts.", self.name)
        self._status = SessionStatus.NOT_CONNECTED

    def _get_session_id(self) -> str:
        if self.session_id:
            return self.session_id
        raise errors.SessionStartError

    async def transfer(self, session_handler: BaseSessionHandler) -> None:
        """Transfer all the players from this session, to a different one.

        !!! warning
            This will close the current sessions connection.

        Parameters
        ----------
        session_handler
            The session handler, that will allow this session to move its players too.
        """
        session = session_handler.fetch_session()
        logger.trace("Transfer players from {} to {}", self.name, session.name)
        for player in self._players.values():
            player = await player.transfer(session)
            session_handler.add_player(player)
        await self.stop()

    async def start(self) -> None:
        """Start the session.

        Starts up the session, to receive events.
        """
        logger.trace("Starting up session {}", self.name)
        self._session_task = asyncio.create_task(self._websocket())

    async def stop(self) -> None:
        """Stop the session.

        Stops the current session, if it is running.
        """
        logger.trace("Shutting down session {}", self.name)
        if self._session_task is None:
            return

        self._session_task.cancel()

        try:
            await self._session_task
        except asyncio.CancelledError:
            self._session_task = None
