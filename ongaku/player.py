"""The player function, for all player related things."""

from __future__ import annotations

import random
import typing
from asyncio import TimeoutError
from asyncio import gather

import hikari
from loguru import logger

from ongaku import errors
from ongaku import events
from ongaku.events import TrackEndReasonType
from ongaku.impl.player import Voice
from ongaku.impl.playlist import Playlist
from ongaku.impl.track import Track

if typing.TYPE_CHECKING:
    from ongaku.impl.filters import Filters
    from ongaku.impl.player import State
    from ongaku.session import Session


__all__ = ("Player",)


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
"""The types you can request for."""


RequestorT: typing.TypeAlias = (
    hikari.SnowflakeishOr[hikari.User] | hikari.SnowflakeishOr[hikari.Member]
)
"""The types to set for a requestor of a track.s"""


class Player:
    """The class that allows the player, to play songs, and more.

    Parameters
    ----------
    session
        The session that the player is attached too.
    guild
        The Guild the bot is attached too.
    """

    __slots__: typing.Sequence[str] = (
        "_autoplay",
        "_channel_id",
        "_connected",
        "_filters",
        "_guild_id",
        "_is_alive",
        "_is_paused",
        "_loop",
        "_position",
        "_queue",
        "_session",
        "_session_id",
        "_state",
        "_voice",
        "_volume",
    )

    def __init__(
        self, session: Session, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        self._session = session
        self._guild_id = hikari.Snowflake(guild)
        self._channel_id: hikari.Snowflake | None = None
        self._is_alive = False
        self._is_paused = True
        self._voice: Voice | None = None
        self._state: State | None = None
        self._queue: typing.MutableSequence[Track] = []
        self._filters: Filters | None = None
        self._connected: bool = False
        self._session_id: str | None = None
        self._volume: int = -1
        self._autoplay: bool = True
        self._position: int = 0
        self._loop = False

        self.app.event_manager.subscribe(
            events.TrackEndEvent, self._track_end_event
        )
        self.app.event_manager.subscribe(
            events.PlayerUpdateEvent, self._player_update_event
        )

    @property
    def session(self) -> Session:
        """The session this player is included in."""
        return self._session

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The session this player is included in."""
        return self.session.client.app

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The `guild id` this player is attached too."""
        return self._guild_id

    @property
    def channel_id(self) -> hikari.Snowflake | None:
        """The `channel id` this player is attached too.

        `None` if not connected to a channel.
        """
        return self._channel_id

    @property
    def is_alive(self) -> bool:
        """Whether the player is alive and attached to lavalink."""
        return self._is_alive

    @property
    def position(self) -> int:
        """The position of the track in milliseconds."""
        return self._position

    @property
    def volume(self) -> int:
        """The volume of the player.

        If `-1` the player has not been connected to lavalink and updated.
        """
        return self._volume

    @property
    def is_paused(self) -> bool:
        """Whether the player is currently paused."""
        return self._is_paused

    @property
    def autoplay(self) -> bool:
        """Whether or not the next song will play, when this song ends."""
        return self._autoplay

    @property
    def loop(self) -> bool:
        """Whether the current track will play again."""
        return self._loop

    @property
    def connected(self) -> bool:
        """Whether or not the player is connected to discords gateway."""
        return self._connected

    @property
    def queue(self) -> typing.Sequence[Track]:
        """The current queue of tracks."""
        return self._queue

    @property
    def voice(self) -> Voice | None:
        """The player's voice state."""
        return self._voice

    @property
    def state(self) -> State | None:
        """The player's player state."""
        return self._state

    @property
    def filters(self) -> Filters | None:
        """Filters for the player."""
        return self._filters

    async def connect(
        self,
        channel: hikari.SnowflakeishOr[hikari.GuildVoiceChannel],
        *,
        mute: bool = False,
        deaf: bool = True,
    ) -> None:
        """Connect the current player to a voice channel.

        Example
        -------
        ```py
        await player.connect(channel_id)
        ```

        Parameters
        ----------
        channel
            The channel (or channel id) that you wish to connect the bot to.
        mute
            Whether or not to mute the player.
        deaf
            Whether or not to deafen the player.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        PlayerConnectError
            Raised when the voice state of the bot cannot be updated, or the voice events required could not be received.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        self._channel_id = hikari.Snowflake(channel)
        logger.debug(
            "Connect to channel: {} guild: {}", self._channel_id, self.guild_id
        )

        try:
            await self.app.update_voice_state(
                self.guild_id, self._channel_id, self_mute=mute, self_deaf=deaf
            )
        except Exception as e:
            raise errors.PlayerConnectError(str(e)) from e

        logger.debug(
            "waiting for voice events for channel: {} in guild: {}",
            self.channel_id,
            self.guild_id,
        )

        try:
            state_event, server_event = await gather(
                self.app.event_manager.wait_for(
                    hikari.VoiceStateUpdateEvent, timeout=5
                ),
                self.app.event_manager.wait_for(
                    hikari.VoiceServerUpdateEvent, timeout=5
                ),
            )
        except TimeoutError as e:
            raise errors.PlayerConnectError(
                f"Could not connect to voice channel {self.channel_id} in {self.guild_id} due to events not being received.",
            ) from e

        if server_event.raw_endpoint is None:
            raise errors.PlayerConnectError(
                f"Endpoint missing for attempted server connection for voice channel {self.channel_id} in {self.guild_id}",
            )

        logger.debug(
            "Received events for channel: {} in guild: {}",
            self.channel_id,
            self.guild_id,
        )

        new_voice = Voice(
            token=server_event.token,
            endpoint=server_event.raw_endpoint,
            session_id=state_event.state.session_id,
        )
        self._voice = new_voice
        self._is_alive = True
        await self._update_player(voice=new_voice, no_replace=False)

    async def disconnect(self) -> None:
        """Disconnect the player from the discord channel, and stop the currently playing track.

        Example
        -------
        ```py
        await player.disconnect()
        ```

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        logger.debug(
            "Delete player for channel: {} in guild: {}",
            self.channel_id,
            self.guild_id,
        )
        await self.clear()
        session = self.session._get_session_id()
        await self.session.client.rest.delete_player(
            session, self._guild_id, session=self.session
        )
        self._is_alive = False
        await self.app.update_voice_state(self.guild_id, None)

    async def play(
        self,
        track: Track | None = None,
        requestor: RequestorT | None = None,
    ) -> None:
        """Play a new track, or start the playing of the queue.

        Example
        -------
        ```py
        await player.play(track)
        ```

        Parameters
        ----------
        track
            The track you wish to play. If none, pulls from the queue.
        requestor
            The member who requested the track.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        PlayerConnectError
            Raised when the player is not connected to a channel.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        if self.channel_id is None:
            raise errors.PlayerConnectError("Not connected to a channel.")

        if len(self.queue) == 0 and track is None:
            raise errors.PlayerQueueError("Queue is empty.")

        if track is not None:
            if requestor is not None:
                track.requestor = hikari.Snowflake(requestor)
            self._queue.insert(0, track)

        self._is_paused = False
        await self._update_player(track=self._queue[0], no_replace=False)

    def add(
        self,
        tracks: typing.Sequence[Track] | Playlist | Track,
        requestor: RequestorT | None = None,
    ) -> None:
        """Add tracks to the queue.

        !!! note
            This will not automatically start playing the songs.
            please call `.play()` after, with no track, if the player is not already playing.

        Example
        -------
        ```py
        await player.add(tracks)
        ```

        Parameters
        ----------
        tracks
            The list of tracks or a singular track you wish to add to the queue.
        requestor
            The user/member who requested the song.
        """
        new_requestor = None
        if requestor is not None:
            new_requestor = hikari.Snowflake(requestor)

        track_count = 0
        if isinstance(tracks, Track):
            tracks.requestor = new_requestor
            self._queue.append(tracks)
            track_count = 1
            return

        if isinstance(tracks, Playlist):
            tracks = tracks.tracks

        for track in tracks:
            track.requestor = new_requestor
            self._queue.append(track)
            track_count += 1

        logger.debug("Added {} track(s) to {}", track_count, self.guild_id)

    async def pause(self, value: bool | None = None) -> None:
        """Allows for the user to pause the currently playing track on this player.

        !!! info
            `True` will force pause the player, `False` will force unpause the player. Leaving it empty, will toggle it from its current state.

        Example
        -------
        ```py
        await player.pause()
        ```

        Parameters
        ----------
        value
            How you wish to pause the bot.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        if value is not None:
            self._is_paused = value
        else:
            self._is_paused = not self.is_paused

        logger.debug(
            "Set paused state to {} in guild {}", self.is_paused, self.guild_id
        )
        await self._update_player(paused=self._is_paused)

    async def stop(self) -> None:
        """Stops the audio, by setting the song to none.

        !!! note
            This does not touch the current queue, just clears the player of its track.

        Example
        -------
        ```py
        await player.stop()
        ```

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        logger.debug("Stopped track in guild {}", self.guild_id)
        self._is_paused = True
        await self._update_player(track=None, no_replace=False)

    def shuffle(self) -> None:
        """Shuffle the current queue.

        !!! note
            This will not touch the first track.

        Raises
        ------
        PlayerQueueError
            Raised when the queue has 2 or less tracks in it.
        """
        if len(self.queue) <= 2:
            raise errors.PlayerQueueError(
                "Queue must have more than 2 tracks to shuffle."
            )

        first_track = self._queue.pop(0)
        random.shuffle(self._queue)
        self._queue.insert(0, first_track)
        logger.debug("Shuffled queue in guild {}", self.guild_id)

    async def skip(self, amount: int = 1) -> None:
        """skip a selected amount of songs in the queue.

        Example
        -------
        ```py
        await player.skip()
        ```

        Parameters
        ----------
        amount
            The amount of songs you wish to skip.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        ValueError
            Raised when the amount set is 0 or negative.
        PlayerQueueError
            Raised when the queue is empty.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        if amount <= 0:
            raise ValueError(
                f"Skip amount cannot be 0 or negative. Value: {amount}"
            )
        if len(self.queue) == 0:
            raise errors.PlayerQueueError("Queue is empty.")

        if amount >= len(self._queue):
            self._queue = []
            track = None
        else:
            for _ in range(amount):
                self._queue.pop(0)
            track = self._queue[0]

        await self._update_player(track=track, no_replace=False)
        logger.debug("Skipped {} track(s) in guild {}", amount, self.guild_id)

    def index(self, track: Track) -> int:
        """Find track in queue and return their index.

        Raises
        ------
        PlayerQueueError
            Raised when the removal of a track fails.
        """
        try:
            return self._queue.index(track)
        except ValueError as e:
            raise errors.PlayerQueueError(
                f"Failed to find song: {track.info.title}",
            ) from e

    def remove(self, value: Track | int) -> None:
        """Removes the track, or the track in that position.

        !!! warning
            This does not stop the track if its in the first position.

        Example
        -------
        ```py
        await player.remove()
        ```

        Parameters
        ----------
        value
            Remove a selected track. If [Track][ongaku.abc.track.Track], then it will remove the first occurrence of that track. If an integer, it will remove the track at that position.

        Raises
        ------
        PlayerQueueError
            Raised when the removal of a track fails.
        """
        if len(self.queue) == 0:
            raise errors.PlayerQueueError("Queue is empty.")

        logger.debug("Remove track {} in {}", value, self.guild_id)
        index = self.index(value) if isinstance(value, Track) else value
        try:
            self._queue.pop(index)
        except IndexError:
            if isinstance(value, Track):
                raise errors.PlayerQueueError(
                    f"Failed to remove song: {value.info.title}",
                )
            raise errors.PlayerQueueError(
                f"Failed to remove song in position {value}",
            )

    async def clear(self) -> None:
        """Clear the current queue, and also stop the audio from the player.

        Example
        -------
        ```py
        player.clear()
        ```

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        logger.debug("Cleared queue in {}", self.guild_id)
        self._queue.clear()
        await self._update_player(track=None, no_replace=False)

    def set_autoplay(self, enable: bool | None = None) -> bool:
        """whether to enable or disable autoplay.

        Example
        -------
        ```py
        await player.set_autoplay()
        ```

        Parameters
        ----------
        enable
            Whether or not to enable autoplay. If left empty, it will toggle the current status.
        """
        if enable is not None:
            self._autoplay = enable
            return self._autoplay

        self._autoplay = not self._autoplay
        return self._autoplay

    async def set_volume(self, volume: int = 100) -> None:
        """The volume you wish to set for the player.

        Example
        -------
        ```py
        await player.set_volume(10)
        ```

        !!! note
            If you don't set a value to volume, it will simply become 100 (The default.)

        Parameters
        ----------
        volume
            The volume you wish to set, from 0 to 1000.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        ValueError
            Raised when the value is below 0, or above 1000.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        if volume < 0 or volume > 1000:
            raise ValueError(f"Volume must be in range 0-1000. (now {volume})")

        logger.debug("Set volume to {} in {}", volume, self.guild_id)
        await self._update_player(volume=volume, no_replace=False)

    async def set_position(self, value: int) -> None:
        """Change the currently playing track's position.

        Example
        -------
        ```py
        await player.set_position(10000)
        ```

        Parameters
        ----------
        value
            The value, of the position, in milliseconds.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        ValueError
            Raised when the position given is negative, or the current tracks length is greater than the length given.
        PlayerQueueError
            Raised when the queue is empty.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        if value <= 0:
            raise ValueError("Negative value is not allowed.")

        if len(self.queue) <= 0:
            raise errors.PlayerQueueError("Queue is empty.")

        if self.queue[0].info.length < value:
            raise ValueError(
                "A value greater than the current tracks length is not allowed.",
            )

        logger.debug("Set position ({}) to track in {}", value, self.guild_id)
        await self._update_player(position=value, no_replace=False)

    async def set_filters(self, filters: Filters | None = None) -> None:
        """Set a new filter for the player.

        Parameters
        ----------
        filters
            The filter to set the player with.
        """
        logger.debug("Updated filters in guild {}", self.guild_id)
        await self._update_player(filters=filters)

    def set_loop(self, enable: bool | None = None) -> bool:
        """whether to enable or disable looping of the current track.

        Example
        -------
        ```py
        await player.set_loop()
        ```

        Parameters
        ----------
        enable
            Whether or not to enable looping. If left empty, it will toggle the current status.
        """
        if enable is not None:
            self._loop = enable
            return self._loop

        self._loop = not self._loop
        return self._loop

    async def transfer(self, session: Session) -> Player:
        """Transfer this player to another session.

        !!! warning
            This will kill the current player, and return a new player.

        Parameters
        ----------
        session
            The session you wish to add the new player to.

        Returns
        -------
        Player
            The new player.
        """
        logger.debug(
            "Transfer player in {} from session ({}) to session ({})",
            self.guild_id,
            self.session.name,
            session.name,
        )
        new_player = Player(session, self.guild_id)
        new_player.add(self.queue)

        if self.connected and self.channel_id:
            await self.disconnect()
            await new_player.connect(self.channel_id)
            if self.is_paused is False:
                await new_player.play()
                await new_player.set_position(self.position)

        return new_player

    async def _update_player(
        self,
        track: hikari.UndefinedNoneOr[Track] = hikari.UNDEFINED,
        position: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        end_time: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        volume: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        paused: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
        filters: hikari.UndefinedNoneOr[Filters] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[Voice] = hikari.UNDEFINED,
        no_replace: bool = True,
    ) -> None:
        logger.debug(
            "Updating player for channel: {} in guild: {}",
            self.channel_id,
            self.guild_id,
        )

        session = self.session._get_session_id()
        player = await self.session.client.rest.update_player(
            session,
            self.guild_id,
            track=track,
            position=position,
            end_time=end_time,
            volume=volume,
            paused=paused,
            filters=filters,
            voice=voice,
            no_replace=no_replace,
            session=self.session,
        )

        logger.debug("New player {}", player)
        self._volume = player.volume
        self._is_paused = player.is_paused
        self._state = player.state
        self._voice = player.voice
        self._filters = player.filters
        self._connected = player.state.connected

    async def _track_end_event(self, event: events.TrackEndEvent) -> None:
        self.session._get_session_id()

        if event.guild_id != self.guild_id or not self.autoplay:
            return

        if (
            event.reason != TrackEndReasonType.FINISHED
            and event.reason != TrackEndReasonType.LOADFAILED
        ):
            return

        logger.debug(
            "Auto-playing track for channel: {} in guild: {}",
            self.channel_id,
            self.guild_id,
        )

        if len(self.queue) == 0:
            logger.debug(
                "queue is empty for channel: {} in guild: {}. Skipping.",
                self.channel_id,
                self.guild_id,
            )
            return

        if len(self.queue) == 1 and not self.loop:
            logger.debug(
                "queue is empty for channel: {} in guild: {}. Dispatching last known track.",
                self.channel_id,
                self.guild_id,
            )
            new_event = events.QueueEmptyEvent(
                self.session.client,
                self.session,
                guild_id=self.guild_id,
                old_track=self.queue[0],
            )

            self.remove(0)
            self.app.event_manager.dispatch(new_event)
            return

        if not self.loop:
            logger.debug(
                "Autoplay for channel: {} in guild: {}. Removing old song.",
                self.channel_id,
                self.guild_id,
            )
            self.remove(0)

        logger.debug(
            "Auto-playing next track for channel: {} in guild: {}. Track title: {}",
            self.channel_id,
            self.guild_id,
            self.queue[0].info.title,
        )
        await self.play()

        self.app.event_manager.dispatch(
            events.QueueNextEvent(
                self.session.client,
                self.session,
                self.guild_id,
                self._queue[0],
                event.track,
            )
        )

    async def _player_update_event(
        self, event: events.PlayerUpdateEvent
    ) -> None:
        if event.guild_id != self.guild_id:
            return
        logger.debug("Updating player state in {}", self.guild_id)

        if not event.state.connected and self.connected:
            await self.stop()

        self._state = event.state
        self._connected = event.state.connected
