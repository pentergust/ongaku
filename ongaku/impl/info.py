"""Information Impl's.

The info implemented classes.
"""

import datetime
import typing

from ongaku.abc import info as info_

__all__ = ("Git", "Info", "Plugin", "Version")


class Info(info_.Info):
    def __init__(
        self,
        version: info_.Version,
        build_time: datetime.datetime,
        git: info_.Git,
        jvm: str,
        lavaplayer: str,
        source_managers: typing.Sequence[str],
        filters: typing.Sequence[str],
        plugins: typing.Sequence[info_.Plugin],
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

        plugins: list[info_.Plugin] = []
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


class Version(info_.Version):
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


class Git(info_.Git):
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


class Plugin(info_.Plugin):
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
