"""Session.

Session related objects.
"""

from __future__ import annotations

import asyncio
import typing

import aiohttp
import hikari
import orjson

from ongaku import errors
from ongaku import events
from ongaku.__metadata__ import __version__
from ongaku.impl.player import State
from ongaku.impl.session import SessionStatus
from ongaku.impl.session import WebsocketEvent
from ongaku.impl.session import WebsocketOPCode
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track
from ongaku.internal import types
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import logger

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.handler.abc import BaseSessionHandler
    from ongaku.player import Player


_logger = logger.getChild("session")


__all__ = ("Session",)


class Session:
    """
    Session.

    The base session object.

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
        """
        The current session id.

        !!! note
            Shows up as none if the current session failed to connect, or has not connected yet.
        """
        return self._session_id

    async def request(
        self,
        method: str,
        path: str,
        return_type: type[types.RequestT] | None,
        *,
        headers: typing.Mapping[str, typing.Any] = {},
        json: typing.Mapping[str, typing.Any]
        | typing.Sequence[typing.Any] = {},
        params: typing.Mapping[str, typing.Any] = {},
        ignore_default_headers: bool = False,
        version: bool = True,
    ) -> types.RequestT | None:
        """Request.

        Make a http(s) request to the current session

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

        if _logger.isEnabledFor(TRACE_LEVEL):
            new_params.update({"trace": "true"})

        _logger.log(
            TRACE_LEVEL,
            f"Making request to {self.base_uri}{'/v4' if version else ''}{path} with headers: {new_headers} and json: {json} and params: {new_params}",
        )

        response = await session.request(
            method,
            f"{self.base_uri}{'/v4' if version else ''}{path}",
            headers=new_headers,
            json=json,
            params=new_params,
        )

        if response.status == 204 and return_type is not None:
            raise errors.RestEmptyError

        if response.status >= 400:
            payload = await response.text()

            if len(payload) == 0:
                raise errors.RestStatusError(response.status, response.reason)

            try:
                rest_error = errors.RestRequestError.from_payload(payload)
            except Exception:
                raise errors.RestStatusError(response.status, response.reason)
            raise rest_error

        if return_type is None:
            return None

        payload = await response.text()

        if issubclass(return_type, str | int | bool | float):
            return return_type(payload)

        try:
            json_payload = orjson.loads(payload)
        except Exception as e:
            raise errors.BuildError(e)

        return return_type(json_payload)

    def _handle_op_code(self, data: str) -> hikari.Event:
        mapped_data = orjson.loads(data)

        if isinstance(mapped_data, typing.Sequence):
            raise errors.BuildError(
                None,
                "Invalid data received. Must be of type 'typing.Mapping' and not 'typing.Sequence'",
            )

        op_code = WebsocketOPCode(mapped_data["op"])

        if op_code == WebsocketOPCode.READY:
            event: events.OngakuEvent = events.ReadyEvent.from_session(
                self, mapped_data["resumed"], mapped_data["sessionId"]
            )
            self._session_id = event.session_id

        elif op_code == WebsocketOPCode.PLAYER_UPDATE:
            event = events.PlayerUpdateEvent.from_session(
                self,
                hikari.Snowflake(int(mapped_data["guildId"])),
                State.from_payload(mapped_data["state"]),
            )

        elif op_code == WebsocketOPCode.STATS:
            stats = Statistics.from_payload(mapped_data)
            event = events.StatisticsEvent.from_session(
                self,
                stats.players,
                stats.playing_players,
                stats.uptime,
                stats.memory,
                stats.cpu,
                stats.frame_stats,
            )

        else:
            event_type = WebsocketEvent(mapped_data["type"])

            if event_type == WebsocketEvent.TRACK_START_EVENT:
                event = events.TrackStartEvent.from_session(
                    self,
                    hikari.Snowflake(int(mapped_data["guildId"])),
                    Track.from_payload(mapped_data["track"]),
                )

            elif event_type == WebsocketEvent.TRACK_END_EVENT:
                event = events.TrackEndEvent.from_session(
                    self,
                    hikari.Snowflake(int(mapped_data["guildId"])),
                    Track.from_payload(mapped_data["track"]),
                    events.TrackEndReasonType(mapped_data["reason"]),
                )

            elif event_type == WebsocketEvent.TRACK_EXCEPTION_EVENT:
                event = events.TrackExceptionEvent.from_session(
                    self,
                    hikari.Snowflake(int(mapped_data["guildId"])),
                    Track.from_payload(mapped_data["track"]),
                    events.TrackExceptionError.from_payload(
                        mapped_data["exception"]
                    ),
                )

            elif event_type == WebsocketEvent.TRACK_STUCK_EVENT:
                event = events.TrackStuckEvent.from_session(
                    self,
                    hikari.Snowflake(int(mapped_data["guildId"])),
                    Track.from_payload(mapped_data["track"]),
                    mapped_data["thresholdMs"],
                )

            else:
                event = events.WebsocketClosedEvent.from_session(
                    self,
                    hikari.Snowflake(int(mapped_data["guildId"])),
                    mapped_data["code"],
                    mapped_data["reason"],
                    mapped_data["byRemote"],
                )

        return event

    def _handle_ws_message(self, msg: aiohttp.WSMessage) -> bool:
        """Returns false if failure or closure, true otherwise."""
        if msg.type == aiohttp.WSMsgType.TEXT:
            payload_event = events.PayloadEvent.from_session(self, msg.data)
            event = self._handle_op_code(msg.data)

            self.app.event_manager.dispatch(payload_event, return_tasks=False)
            self.app.event_manager.dispatch(event, return_tasks=False)

            return True

        if msg.type == aiohttp.WSMsgType.ERROR:
            _logger.warning("An error occurred.")

        elif msg.type == aiohttp.WSMsgType.CLOSED:
            _logger.warning(
                f"Told to close. Code: {msg.data.name}. Message: {msg.extra}",
            )

        return False

    async def _websocket(self) -> None:
        bot = self.app.get_me()

        _logger.log(
            TRACE_LEVEL,
            f"Attempting to start websocket connection to session {self.name}",
        )

        if not bot:
            if self._remaining_attempts > 0:
                self._status = SessionStatus.NOT_CONNECTED

                _logger.warning(
                    "Attempted fetching the bot, but failed as it does not exist.",
                )
            else:
                self._status = SessionStatus.FAILURE

            _logger.warning(
                "Attempted fetching the bot, but failed as it does not exist.",
            )

            raise errors.SessionStartError

        self._websocket_headers = {
            "User-Id": str(int(bot.id)),
            "Client-Name": f"{bot.global_name if bot.global_name else 'unknown'}/{__version__}",
        }

        new_headers: typing.MutableMapping[str, typing.Any] = {}

        new_headers.update(self._websocket_headers)

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
                    _logger.log(
                        TRACE_LEVEL,
                        f"Successfully made connection to session {self.name}",
                    )
                    self._status = SessionStatus.CONNECTED
                    while True:
                        msg = await ws.receive()

                        if self._handle_ws_message(msg) is False:
                            self._status = SessionStatus.FAILURE
                            await self.transfer(self.client.session_handler)
                            return

            except Exception as e:
                _logger.warning(f"Websocket connection failure: {e}")
                self._status = SessionStatus.NOT_CONNECTED
                break

        else:
            _logger.warning(f"Session {self.name} has no more attempts.")
            self._status = SessionStatus.NOT_CONNECTED

    def _get_session_id(self) -> str:
        if self.session_id:
            return self.session_id

        raise errors.SessionStartError

    async def transfer(self, session_handler: BaseSessionHandler) -> None:
        """
        Transfer.

        Transfer all the players from this session, to a different one.

        !!! warning
            This will close the current sessions connection.

        Parameters
        ----------
        session_handler
            The session handler, that will allow this session to move its players too.
        """
        session = session_handler.fetch_session()

        _logger.log(
            TRACE_LEVEL,
            f"Attempting transfer players from session {self.name} to {session.name}",
        )

        for player in self._players.values():
            player = await player.transfer(session)

            session_handler.add_player(player)

        await self.stop()

        _logger.log(
            TRACE_LEVEL,
            f"Successfully transferred and stopped session {self.name} and moved players to session {session.name}",
        )

    async def start(self) -> None:
        """
        Start the session.

        Starts up the session, to receive events.
        """
        _logger.log(
            TRACE_LEVEL,
            f"Starting up session {self.name}",
        )
        self._session_task = asyncio.create_task(self._websocket())
        _logger.log(
            TRACE_LEVEL,
            f"Successfully started session {self.name}",
        )

    async def stop(self) -> None:
        """
        Stop the session.

        Stops the current session, if it is running.
        """
        _logger.log(
            TRACE_LEVEL,
            f"Shutting down session {self.name}",
        )
        if self._session_task:
            self._session_task.cancel()

            try:
                await self._session_task
            except asyncio.CancelledError:
                self._session_task = None

        _logger.log(
            TRACE_LEVEL,
            f"Successfully shut down session {self.name}",
        )
