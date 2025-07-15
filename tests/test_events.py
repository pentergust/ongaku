from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import hikari

from ongaku import events
from ongaku.errors import SeverityType
from ongaku.events import TrackEndReasonType
from ongaku.impl import player

if TYPE_CHECKING:
    from hikari.impl import gateway_bot as gateway_bot_

    from ongaku.client import Client
    from ongaku.impl.track import Track
    from ongaku.session import Session


class TestEventBuilds:
    def test_payload(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        event = events.PayloadEvent(ongaku_client, ongaku_session, "payload")

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.payload == "payload"

    def test_ready(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        event = events.ReadyEvent(
            ongaku_client, ongaku_session, False, "session_id"
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.resumed is False
        assert event.session_id == "session_id"

    def test_payload_update(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        state = player.State(datetime.datetime.now(), 2, False, 3)
        event = events.PlayerUpdateEvent(
            ongaku_client, ongaku_session, hikari.Snowflake(1234567890), state
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.state == state

    def test_websocket_closed(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        event = events.WebsocketClosedEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            1,
            "reason",
            False,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.code == 1
        assert event.reason == "reason"
        assert event.by_remote is False

    def test_track_start(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
        ongaku_track: Track,
    ):
        event = events.TrackStartEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            ongaku_track,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.track == ongaku_track

    def test_track_end(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
        ongaku_track: Track,
    ):
        event = events.TrackEndEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            ongaku_track,
            TrackEndReasonType.FINISHED,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.track == ongaku_track
        assert event.reason == TrackEndReasonType.FINISHED

    def test_track_error(self):
        exception = events.TrackExceptionError(
            "message", SeverityType.COMMON, "cause"
        )

        assert exception.message == "message"
        assert exception.severity == SeverityType.COMMON
        assert exception.cause == "cause"

    def test_track_exception(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
        ongaku_track: Track,
    ):
        exception = events.TrackExceptionError(
            "message", SeverityType.COMMON, "cause"
        )
        event = events.TrackExceptionEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            ongaku_track,
            exception,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.track == ongaku_track
        assert event.exception == exception

    def test_track_stuck(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
        ongaku_track: Track,
    ):
        event = events.TrackStuckEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            ongaku_track,
            1,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.track == ongaku_track
        assert event.threshold_ms == 1

    def test_queue_empty(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
        ongaku_track: Track,
    ):
        event = events.QueueEmptyEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            ongaku_track,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.old_track == ongaku_track

    def test_queue_next(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        ongaku_session: Session,
        ongaku_track: Track,
    ):
        event = events.QueueNextEvent(
            ongaku_client,
            ongaku_session,
            hikari.Snowflake(1234567890),
            ongaku_track,
            ongaku_track,
        )

        assert event.app == gateway_bot
        assert event.client == ongaku_client
        assert event.session == ongaku_session
        assert event.guild_id == hikari.Snowflake(1234567890)
        assert event.old_track == ongaku_track
        assert event.track == ongaku_track
