"""Information Impl's.

The info implemented classes.
"""

import datetime
import typing

from ongaku.impl.payload import PayloadObject

__all__ = ("Git", "Info", "Plugin", "Version")


class Version(PayloadObject):
    """
    Version information.

    All information, about the version of lavalink that is running.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#version-object)
    """

    __slots__: typing.Sequence[str] = (
        "_build",
        "_major",
        "_minor",
        "_patch",
        "_pre_release",
        "_semver",
    )

    def __init__(
        self,
        semver: str,
        major: int,
        minor: int,
        patch: int,
        pre_release: str,
        build: str | None,
    ) -> None:
        self._semver = semver
        self._major = major
        self._minor = minor
        self._patch = patch
        self._pre_release = pre_release
        self._build = build

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

    @property
    def semver(self) -> str:
        """The full version string of this Lavalink server."""
        return self._semver

    @property
    def major(self) -> int:
        """The major version of this Lavalink server."""
        return self._major

    @property
    def minor(self) -> int:
        """The minor version of this Lavalink server."""
        return self._minor

    @property
    def patch(self) -> int:
        """The patch version of this Lavalink server."""
        return self._patch

    @property
    def pre_release(self) -> str:
        """The pre-release version according to semver as a `.` separated list of identifiers."""
        return self._pre_release

    @property
    def build(self) -> str | None:
        """The build metadata according to semver as a `.` separated list of identifiers."""
        return self._build

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False

        if self.semver != other.semver:
            return False

        if self.major != other.major:
            return False

        if self.minor != other.minor:
            return False

        if self.patch != other.patch:
            return False

        if self.pre_release != other.pre_release:
            return False

        return self.build == other.build


class Git(PayloadObject):
    """
    Git information.

    All of the information about the lavalink git information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#git-object)
    """

    __slots__: typing.Sequence[str] = (
        "_branch",
        "_commit",
        "_commit_time",
    )

    def __init__(
        self,
        branch: str,
        commit: str,
        commit_time: datetime.datetime,
    ) -> None:
        self._branch = branch
        self._commit = commit
        self._commit_time = commit_time

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

    @property
    def branch(self) -> str:
        """The branch this Lavalink server was built on."""
        return self._branch

    @property
    def commit(self) -> str:
        """The commit this Lavalink server was built on."""
        return self._commit

    @property
    def commit_time(self) -> datetime.datetime:
        """The datetime object of when the commit was created."""
        return self._commit_time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Git):
            return False

        if self.branch != other.branch:
            return False

        if self.commit != other.commit:
            return False

        return self.commit_time == other.commit_time


class Plugin(PayloadObject):
    """
    Plugin information.

    All of the Information about the currently loaded plugins.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#plugin-object)
    """

    __slots__: typing.Sequence[str] = ("_name", "_version")

    def __init__(self, name: str, version: str) -> None:
        self._name = name
        self._version = version

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

    @property
    def name(self) -> str:
        """The name of the plugin."""
        return self._name

    @property
    def version(self) -> str:
        """The version of the plugin."""
        return self._version

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Plugin):
            return False

        if self.name != other.name:
            return False

        return self.version == other.version


class Info(PayloadObject):
    """
    Information.

    All of the Info Version information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#info-response)
    """

    __slots__: typing.Sequence[str] = (
        "_build_time",
        "_filters",
        "_git",
        "_jvm",
        "_lavaplayer",
        "_plugins",
        "_source_managers",
        "_version",
    )

    def __init__(
        self,
        version: Version,
        build_time: datetime.datetime,
        git: Git,
        jvm: str,
        lavaplayer: str,
        source_managers: typing.Sequence[str],
        filters: typing.Sequence[str],
        plugins: typing.Sequence[Plugin],
    ) -> None:
        self._version = version
        self._build_time = build_time
        self._git = git
        self._jvm = jvm
        self._lavaplayer = lavaplayer
        self._source_managers = source_managers
        self._filters = filters
        self._plugins = plugins

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

    @property
    def version(self) -> Version:
        """The version of this Lavalink server."""
        return self._version

    @property
    def build_time(self) -> datetime.datetime:
        """The datetime object of when this Lavalink jar was built."""
        return self._build_time

    @property
    def git(self) -> Git:
        """The git information of this Lavalink server."""
        return self._git

    @property
    def jvm(self) -> str:
        """The JVM version this Lavalink server runs on."""
        return self._jvm

    @property
    def lavaplayer(self) -> str:
        """The Lavaplayer version being used by this server."""
        return self._lavaplayer

    @property
    def source_managers(self) -> typing.Sequence[str]:
        """The enabled source managers for this server."""
        return self._source_managers

    @property
    def filters(self) -> typing.Sequence[str]:
        """The enabled filters for this server."""
        return self._filters

    @property
    def plugins(self) -> typing.Sequence[Plugin]:
        """The enabled plugins for this server."""
        return self._plugins

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Info):
            return False

        if self.version != other.version:
            return False

        if self.build_time != other.build_time:
            return False

        if self.git != other.git:
            return False

        if self.jvm != other.jvm:
            return False

        if self.lavaplayer != other.lavaplayer:
            return False

        if self.source_managers != other.source_managers:
            return False

        if self.filters != other.filters:
            return False

        return self.plugins == other.plugins
