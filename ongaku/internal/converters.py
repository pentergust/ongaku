"""Converters.

All internal converters.

TODO: Use orjson directly
"""

import typing

__all__ = ("json_dumps", "json_loads")

DumpType = typing.Callable[
    [typing.Sequence[typing.Any] | typing.Mapping[str, typing.Any]],
    bytes,
]
"""The json dump type."""

json_dumps: DumpType
"""The json dumper."""

LoadType = typing.Callable[
    [str | bytes],
    typing.Sequence[typing.Any] | typing.Mapping[str, typing.Any],
]
"""The json load type."""

json_loads: LoadType
"""The json loader."""

try:
    import orjson

    json_dumps = orjson.dumps
    json_loads = orjson.loads

except ModuleNotFoundError:
    import json

    def basic_json_dumps(
        obj: typing.Sequence[typing.Any] | typing.Mapping[str, typing.Any],
    ) -> bytes:
        """Encode a JSON object to a str."""
        return json.dumps(obj).encode("utf-8")

    json_dumps = basic_json_dumps
    json_loads = json.loads
