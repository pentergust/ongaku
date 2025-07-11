"""Information Impl's.

The info implemented classes.
"""

import datetime
import typing
from dataclasses import dataclass

from ongaku.impl.payload import PayloadObject

__all__ = ("Git", "Info", "Plugin", "Version")


@dataclass(order=True, frozen=True, slots=True)
class Version(PayloadObject):
    """Version information.

    All information, about the version of lavalink that is running.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#version-object)
    """

    semver: str
    """The full version string of this Lavalink server."""

    major: int
    """The major version of this Lavalink server."""

    minor: int
    """The minor version of this Lavalink server."""

    patch: int
    """The patch version of this Lavalink server."""

    pre_release: str
    """The pre-release version according to semver as a `.` separated list of identifiers."""

    build: str | None
    """The build metadata according to semver as a `.` separated list of identifiers."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Version":
        """Build Version Information from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Version(
            payload["semver"],
            payload["major"],
            payload["minor"],
            payload["patch"],
            payload["preRelease"],
            payload.get("build", None),
        )


@dataclass(order=True, frozen=True, slots=True)
class Git(PayloadObject):
    """Git information.

    All of the information about the lavalink git information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#git-object)
    """

    branch: str
    """The branch this Lavalink server was built on."""

    commit: str
    """The commit this Lavalink server was built on."""

    commit_time: datetime.datetime
    """The datetime object of when the commit was created."""

    @classmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> "Git":
        """Build Git Information from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Git(
            payload["branch"],
            payload["commit"],
            datetime.datetime.fromtimestamp(
                int(payload["commitTime"]) / 1000,
                datetime.timezone.utc,
            ),
        )


@dataclass(order=True, frozen=True, slots=True)
class Plugin(PayloadObject):
    """Plugin information.

    All of the Information about the currently loaded plugins.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#plugin-object)
    """

    name: str
    """The name of the plugin."""

    version: str
    """The version of the plugin."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Plugin":
        """Build Plugin Information from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        return Plugin(payload["name"], payload["version"])


@dataclass(order=True, frozen=True, slots=True)
class Info(PayloadObject):
    """Information.

    All of the Info Version information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#info-response)
    """

    version: Version
    """The version of this Lavalink server."""

    build_time: datetime.datetime
    """The datetime object of when this Lavalink jar was built."""

    git: Git
    """The git information of this Lavalink server."""

    jvm: str
    """The JVM version this Lavalink server runs on."""

    lavaplayer: str
    """The Lavaplayer version being used by this server."""

    source_managers: typing.Sequence[str]
    """The enabled source managers for this server."""

    filters: typing.Sequence[str]
    """The enabled filters for this server."""

    plugins: typing.Sequence[Plugin]
    """The enabled plugins for this server."""

    @classmethod
    def _from_payload(cls, payload: typing.Mapping[str, typing.Any]) -> "Info":
        """Build Information from payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        source_managers: list[str] = []
        for manager in payload["sourceManagers"]:
            source_managers.append(manager)

        filters: list[str] = []
        for filter in payload["filters"]:
            filters.append(filter)

        plugins: list[Plugin] = []
        for plugin in payload["plugins"]:
            plugins.append(Plugin.from_payload(plugin))

        return Info(
            Version.from_payload(payload["version"]),
            datetime.datetime.fromtimestamp(
                int(payload["buildTime"]) / 1000,
                datetime.timezone.utc,
            ),
            Git.from_payload(payload["git"]),
            payload["jvm"],
            payload["lavaplayer"],
            source_managers,
            filters,
            plugins,
        )
