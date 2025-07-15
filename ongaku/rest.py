"""Rest client.

All REST based actions, happen in here.
"""

from __future__ import annotations

import typing

import hikari
from loguru import logger

from ongaku import errors
from ongaku import routes
from ongaku.impl.info import Info
from ongaku.impl.player import Player
from ongaku.impl.playlist import Playlist
from ongaku.impl.routeplanner import RoutePlannerStatus
from ongaku.impl.session import Session as SessionData
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track
from ongaku.session import Session

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.impl.filters import Filters
    from ongaku.impl.player import Voice


__all__ = ("RESTClient",)


class RESTClient:
    """The base REST client, for all rest related actions.

    !!! warning
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    __slots__: typing.Sequence[str] = "_client"

    def __init__(self, client: Client) -> None:
        self._client = client

    async def load_track(
        self, query: str, *, session: Session | None = None
    ) -> Playlist | typing.Sequence[Track] | Track | None:
        """Loads tracks from a site, a playlist or a track, to play on a player.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#track-loading)

        Example
        -------
        ```py
        track = await client.rest.load_track("ytsearch:ajr")

        await player.play(track)
        ```

        Parameters
        ----------
        query
            The query for the search/link.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track, playlist or search could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Track]
            A sequence of tracks (a search result)
        Playlist
            A Playlist object.
        Track
            A Track object.
        None
            No result was returned.
        """
        route = routes.GET_LOAD_TRACKS
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method, route.path, dict, params={"identifier": query}
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        load_type: str = response["loadType"]
        if load_type == "empty":
            logger.trace("loadType is empty.")
            return None

        if load_type == "error":
            logger.trace("loadType caused an error.")
            raise errors.RestExceptionError.from_payload(response["data"])

        if load_type == "search":
            logger.trace("loadType was a search result.")
            build = [Track.from_payload(track) for track in response["data"]]

        elif load_type == "track":
            logger.trace("loadType was a track link.")
            build = Track.from_payload(response["data"])

        elif load_type == "playlist":
            logger.trace("loadType was a playlist link.")
            build = Playlist.from_payload(response["data"])

        else:
            raise errors.BuildError(
                None, f"An unknown loadType was received: {load_type}"
            )

        return build

    async def decode_track(
        self, track: str, *, session: Session | None = None
    ) -> Track:
        """Decode a track from its encoded state.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#track-decoding)

        Example
        -------
        ```py
        track = await client.rest.decode_track(BASE64)

        await player.play(track)
        ```

        Parameters
        ----------
        track
            The BASE64 code, from a previously encoded track.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track could not be built
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Track
            The Track object.
        """
        route = routes.GET_DECODE_TRACK
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method,
            route.path,
            dict,
            params={"encodedTrack": track},
        )

        if response is None:
            raise ValueError("Response is required for this request.")
        return Track.from_payload(response)

    async def decode_tracks(
        self, tracks: typing.Sequence[str], *, session: Session | None = None
    ) -> typing.Sequence[Track]:
        """Decode multiple tracks from their encoded state.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#track-decoding)

        Example
        -------
        ```py
        tracks = await client.rest.decode_tracks([BASE64_1, BASE64_2])

        await player.add(tracks)
        ```

        Parameters
        ----------
        tracks
            The BASE64 codes, from all the previously encoded tracks.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the tracks could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Track]
            The Track object.
        """
        route = routes.POST_DECODE_TRACKS
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method,
            route.path,
            list,
            headers={"Content-Type": "application/json"},
            json=tracks,
        )

        if response is None:
            raise ValueError("Response is required for this request.")
        return [Track.from_payload(payload) for payload in response]

    async def fetch_players(
        self, session_id: str, *, session: Session | None = None
    ) -> typing.Sequence[Player]:
        """Fetches all players on this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-players)

        Example
        -------
        ```py
        players = await client.rest.fetch_players(session_id)

        for player in players:
            print(player.guild_id)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the players could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Player]
            The Sequence of player objects.
        """
        route = routes.GET_PLAYERS
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method,
            route.path.format(session_id=session_id),
            list,
        )

        if response is None:
            raise ValueError("Response is required for this request.")
        return [Player.from_payload(payload) for payload in response]

    async def fetch_player(
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.Guild],
        *,
        session: Session | None = None,
    ) -> Player:
        """Fetches a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-player)

        Example
        -------
        ```py
        player = await client.rest.fetch_player(session_id, guild_id)

        print(player.volume)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        guild
            The `guild` or `guild id` that the player is attached to.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the player could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Player
            The player object.
        """
        route = routes.GET_PLAYER
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method,
            route.path.format(
                session_id=session_id, guild_id=hikari.Snowflake(guild)
            ),
            dict,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return Player.from_payload(response)

    async def update_player(  # noqa: C901
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.Guild],
        *,
        track: hikari.UndefinedNoneOr[Track] = hikari.UNDEFINED,
        position: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        end_time: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        volume: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        paused: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
        filters: hikari.UndefinedNoneOr[Filters] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[Voice] = hikari.UNDEFINED,
        no_replace: bool = True,
        session: Session | None = None,
    ) -> Player:
        """Fetches a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#update-player)

        !!! tip
            Setting any value (except for `session_id`, or `guild_id`) to None, will set their values to None.
            To not modify them, do not set them to anything.

        !!! warning
            If you do not set any value (not including `session_id` or `guild_id` as they are required) you will receive a `ValueError`

        Example
        -------
        ```py
        await client.rest.update_player(session_id, guild_id, paused=True)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        guild
            The `guild` or `guild id` that the player is attached to.
        track
            The track you wish to set, or remove
        position
            The new position for the track.
        end_time
            The end time for the track.
        volume
            The volume of the player.
        paused
            Whether or not to pause the player.
        filters
            The filters to apply to the player.
        voice
            The player voice object you wish to set.
        no_replace
            Whether or not the track can be replaced.
        session
            If provided, the session to use for this request.

        Raises
        ------
        ValueError
            Raised when nothing new has been set.
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track, playlist or search could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Player
            The player object.
        """
        if (
            track is hikari.UNDEFINED
            and position is hikari.UNDEFINED
            and end_time is hikari.UNDEFINED
            and volume is hikari.UNDEFINED
            and paused is hikari.UNDEFINED
            and filters is hikari.UNDEFINED
            and voice is hikari.UNDEFINED
        ):
            raise ValueError("Update requires at least one change.")

        patch_data: typing.MutableMapping[str, typing.Any] = {}
        if track != hikari.UNDEFINED:
            if track is None:
                patch_data["track"] = {"encoded": None}
            else:
                track_data: dict[str, typing.Any] = {"encoded": track.encoded}
                user_data = dict(track.user_data)
                if track.requestor is not None:
                    user_data["ongaku_requestor"] = str(track.requestor)

                track_data["userData"] = user_data
                patch_data["track"] = track_data

        if position != hikari.UNDEFINED:
            patch_data["position"] = position

        if end_time != hikari.UNDEFINED:
            patch_data["endTime"] = end_time

        if volume != hikari.UNDEFINED:
            patch_data["volume"] = volume

        if paused != hikari.UNDEFINED:
            patch_data["paused"] = paused

        if filters != hikari.UNDEFINED:
            patch_data["filters"] = None if filters is None else filters.dump()

        if voice != hikari.UNDEFINED:
            patch_data["voice"] = {
                "token": voice.token,
                "endpoint": voice.endpoint,
                "sessionId": voice.session_id,
            }

        route = routes.PATCH_PLAYER_UPDATE
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method,
            route.path.format(
                session_id=session_id, guild_id=hikari.Snowflake(guild)
            ),
            dict,
            headers={"Content-Type": "application/json"},
            json=patch_data,
            params={"noReplace": "true" if no_replace else "false"},
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return Player.from_payload(response)

    async def delete_player(
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.Guild],
        session: Session | None = None,
    ) -> None:
        """
        Delete a player.

        Deletes a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#destroy-player)

        Example
        -------
        ```py
        await client.rest.delete_player(session_id, guild_id)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        guild
            The `guild` or `guild id` that the player is attached to.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.DELETE_PLAYER
        session = session or self._client.session_handler.fetch_session()
        await session.request(
            route.method,
            route.path.format(
                session_id=session_id, guild_id=hikari.Snowflake(guild)
            ),
            None,
        )

    async def update_session(
        self,
        session_id: str,
        *,
        resuming: bool | None = None,
        timeout: int | None = None,
        session: Session | None = None,
    ) -> SessionData:
        """Updates the lavalink session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#update-session)

        Example
        -------
        ```py
        await client.rest.update_session(session_id, False)
        ```

        Parameters
        ----------
        session_id
            The session you wish to update.
        resuming
            Whether resuming is enabled for this session or not.
        timeout
            The timeout in seconds (default is 60s)
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the session could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Session
            The Session object.
        """
        route = routes.PATCH_SESSION_UPDATE
        session = session or self._client.session_handler.fetch_session()
        data: typing.MutableMapping[str, typing.Any] = {}

        if resuming is not None:
            data["resuming"] = resuming

        if timeout is not None:
            data["timeout"] = timeout

        response = await session.request(
            route.method,
            route.path.format(session_id=session_id),
            dict,
            headers={"Content-Type": "application/json"},
            json=data,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return SessionData.from_payload(response)

    async def fetch_info(self, *, session: Session | None = None) -> Info:
        """Gets the current sessions information.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-info)

        Example
        -------
        ```py
        info = await client.rest.fetch_info()

        print(info.version.semver)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the information could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Info
            The Info object.
        """
        route = routes.GET_INFO
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(route.method, route.path, dict)
        if response is None:
            raise ValueError("Response is required for this request.")

        return Info.from_payload(response)

    async def fetch_version(self, *, session: Session | None = None) -> str:
        """Gets the current Lavalink version.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-version)

        Example
        -------
        ```py
        version = await client.rest.fetch_version()

        print(version)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        str
            The version, in string format.
        """
        route = routes.GET_VERSION
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(
            route.method, route.path, str, version=False
        )
        if response is None:
            raise ValueError("Response is required for this request.")
        return response

    async def fetch_stats(
        self, *, session: Session | None = None
    ) -> Statistics:
        """
        Get statistics.

        Gets the current Lavalink statistics.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-stats)

        !!! note
            frame_statistics will always be `None`.

        Example
        -------
        ```py
        stats = await client.rest.fetch_stats()

        print(stats.players)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the statistics could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Statistics
            The Statistics object.
        """
        route = routes.GET_STATISTICS
        session = session or self._client.session_handler.fetch_session()
        response = await session.request(route.method, route.path, dict)
        if response is None:
            raise ValueError("Response is required for this request.")
        return Statistics.from_payload(response)

    async def fetch_routeplanner_status(
        self, *, session: Session | None = None
    ) -> RoutePlannerStatus | None:
        """Fetch routeplanner status.

        Fetches the routeplanner status of the current session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-routeplanner-status)

        Example
        -------
        ```py
        routeplanner_status = await client.rest.fetch_routeplanner_status()

        if routeplanner_status:
            print(routeplanner_status.class_type.name)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the routeplanner status could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        RoutePlannerStatus
            The RoutePlannerStatus object.
        None
            The Route Planner for this server is not active.
        """
        route = routes.GET_ROUTEPLANNER_STATUS
        session = session or self._client.session_handler.fetch_session()
        try:
            response = await session.request(route.method, route.path, dict)
        except errors.RestEmptyError as e:
            logger.warning(e)
            response = None

        if response is None:
            return None

        return RoutePlannerStatus.from_payload(response)

    async def update_routeplanner_address(
        self, address: str, *, session: Session | None = None
    ) -> None:
        """Free routeplanner address.

        Free's the specified routeplanner address.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#unmark-a-failed-address)

        Example
        -------
        ```py
        await client.rest.update_routeplanner_address(address)
        ```

        Parameters
        ----------
        address
            The address you wish to free.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.POST_ROUTEPLANNER_FREE_ADDRESS
        session = session or self._client.session_handler.fetch_session()
        await session.request(
            route.method, route.path, None, json={"address": address}
        )

    async def update_all_routeplanner_addresses(
        self, *, session: Session | None = None
    ) -> None:
        """Free all routeplanner addresses.

        Frees every blocked routeplanner address.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#unmark-all-failed-address)

        Example
        -------
        ```py
        await client.rest.update_all_routeplanner_addresses()
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.POST_ROUTEPLANNER_FREE_ALL
        session = session or self._client.session_handler.fetch_session()
        await session.request(route.method, route.path, None)
