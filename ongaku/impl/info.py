"""Information Impl's.

The info implemented classes.
"""

import typing

from ongaku.abc import info as info_

if typing.TYPE_CHECKING:
    import datetime

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


class Plugin(info_.Plugin):
    def __init__(self, name: str, version: str) -> None:
        self._name = name
        self._version = version
