import typing
from dataclasses import dataclass
from enum import IntEnum

from typing_extensions import Self

from ongaku.impl.payload import PayloadObject

__all__ = ("BandType", "Filters")


def _clear_payload(res: dict[str, typing.Any]) -> dict[str, typing.Any] | None:
    clear_res = {k: v for k, v in res.items() if v is not None}
    return clear_res if len(clear_res) > 0 else None


class BandType(IntEnum):
    """Band Type.

    All the available band types.
    """

    HZ25 = 0
    """25 Hz"""
    HZ40 = 1
    """40 Hz"""
    HZ63 = 2
    """63 Hz"""
    HZ100 = 3
    """100 Hz"""
    HZ160 = 4
    """160 Hz"""
    HZ250 = 5
    """250 Hz"""
    HZ400 = 6
    """400 Hz"""
    HZ630 = 7
    """630 Hz"""
    HZ1000 = 8
    """1000 Hz"""
    HZ1600 = 9
    """1600 Hz"""
    HZ2500 = 10
    """2500 Hz"""
    HZ4000 = 11
    """4000 Hz"""
    HZ6300 = 12
    """6300 Hz"""
    HZ10000 = 13
    """10000 Hz"""
    HZ16000 = 14
    """16000 Hz"""


@dataclass(order=True, frozen=True, slots=True)
class Equalizer(PayloadObject):
    """Equalizer.

    There are 15 bands (0-14) that can be changed.
    "gain" is the multiplier for the given band.
    The default value is 0. Valid values range from -0.25 to 1.0,
    where -0.25 means the given band is completely muted, and 0.25 means it is doubled.
    Modifying the gain could also change the volume of the output.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#equalizer)
    """

    band: BandType
    """The band (0 to 14)."""

    gain: float
    """The gain (-0.25 to 1.0)."""

    def __post_init__(self) -> None:
        if self.gain > 1 or self.gain < -0.25:
            raise ValueError("Gain must be in range (-0.25; 1).")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Equalizer":
        return Equalizer(BandType(payload["band"]), payload["gain"])

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use in rest."""
        return {"band": self.band.value, "gain": self.gain}


@dataclass(order=True, frozen=True, slots=True)
class Karaoke(PayloadObject):
    """Karaoke.

    Uses equalization to eliminate part of a band, usually targeting vocals.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#karaoke)
    """

    level: float | None
    """The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""

    mono_level: float | None
    """The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""

    filter_band: float | None
    """The filter band (in Hz)."""

    filter_width: float | None
    """The filter width."""

    def __post_init__(self) -> None:
        if self.level is not None and (self.level > 1 or self.level < 0):
            raise ValueError("Level must be at in range (0; 1).")

        if self.mono_level is not None and (
            self.mono_level > 1 or self.mono_level < 0
        ):
            raise ValueError("MonoLevel must be in range (0; 1).")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Karaoke":
        return Karaoke(
            payload.get("level", None),
            payload.get("monoLevel", None),
            payload.get("filterBand", None),
            payload.get("filterWidth", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload(
            {
                "level": self.level,
                "monoLevel": self.mono_level,
                "filterBand": self.filter_band,
                "filterWidth": self.filter_width,
            }
        )


@dataclass(order=True, frozen=True, slots=True)
class Timescale(PayloadObject):
    """Timescale.

    Changes the speed, pitch, and rate. All default to 1.0.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#timescale)
    """

    speed: float | None
    """The playback speed 0.0 ≤ x."""

    pitch: float | None
    """The pitch 0.0 ≤ x."""

    rate: float | None
    """The rate 0.0 ≤ x."""

    def __post_init__(self) -> None:
        if self.speed is not None and self.speed < 0:
            raise ValueError("Speed must be at or above 0.")
        if self.pitch is not None and self.pitch < 0:
            raise ValueError("Pitch must be at or above 0.")
        if self.rate is not None and self.rate < 0:
            raise ValueError("Rate must be at or above 0.")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Timescale":
        return Timescale(
            payload.get("speed", None),
            payload.get("pitch", None),
            payload.get("rate", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload(
            {"speed": self.speed, "pitch": self.pitch, "rate": self.rate}
        )


@dataclass(order=True, frozen=True, slots=True)
class Tremolo(PayloadObject):
    """Tremolo.

    Uses amplification to create a shuddering effect, where the volume quickly oscillates.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#tremolo)
    """

    frequency: float | None
    """The frequency 0.0 < x."""

    depth: float | None
    """The tremolo depth 0.0 < x ≤ 1.0."""

    def __post_init__(self) -> None:
        if self.frequency is not None and self.frequency < 0:
            raise ValueError("Frequency must be at or above 0.")

        if self.depth is not None and (self.depth > 1 or self.depth < 0):
            raise ValueError("Depth must be in range (0; 1).")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Tremolo":
        """Build tremolo filter from payload."""
        return Tremolo(
            payload.get("frequency", None),
            payload.get("depth", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload(
            {"frequency": self.frequency, "depth": self.depth}
        )


@dataclass(order=True, frozen=True, slots=True)
class Vibrato(PayloadObject):
    """Vibrato.

    Similar to tremolo. While tremolo oscillates the volume, vibrato oscillates the pitch.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#vibrato)
    """

    frequency: float | None
    """The frequency 0.0 < x ≤ 14.0."""

    depth: float | None
    """The vibrato depth 0.0 < x ≤ 1.0."""

    def __post_init__(self) -> None:
        if self.frequency is not None and (
            self.frequency > 14 or self.frequency < 0
        ):
            raise ValueError("Frequency must be in range  (0; 14).")

        if self.depth is not None and (self.depth > 1 or self.depth < 0):
            raise ValueError("Depth must be in range  (0; 1).")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Vibrato":
        """Build vibrato filter from payload."""
        return Vibrato(
            payload.get("frequency", None),
            payload.get("depth", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload(
            {"frequency": self.frequency, "depth": self.depth}
        )


@dataclass(order=True, frozen=True, slots=True)
class Rotation(PayloadObject):
    """Rotation.

    Rotates the sound around the stereo channels/user headphones (aka Audio Panning).

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#rotation)
    """

    rotation_hz: float | None
    """The frequency of the audio rotating around the listener in Hz."""

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Rotation":
        """Build rotation filter from payload."""
        return Rotation(
            payload.get("rotationHz", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload({"rotationHz": self.rotation_hz})


@dataclass(order=True, frozen=True, slots=True)
class Distortion(PayloadObject):
    """Distortion.

    Distortion effect. It can generate some pretty unique audio effects.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#distortion)
    """

    sin_offset: float | None
    sin_scale: float | None
    cos_offset: float | None
    cos_scale: float | None
    tan_offset: float | None
    tan_scale: float | None
    offset: float | None
    scale: float | None

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Distortion":
        """Build distortion filter from payload."""
        return Distortion(
            payload.get("sinOffset", None),
            payload.get("sinScale", None),
            payload.get("cosOffset", None),
            payload.get("cosScale", None),
            payload.get("tanOffset", None),
            payload.get("tanScale", None),
            payload.get("offset", None),
            payload.get("scale", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload(
            {
                "sinOffset": self.sin_offset,
                "sinScale": self.sin_scale,
                "cosOffset": self.cos_offset,
                "cosScale": self.cos_scale,
                "tanOffset": self.tan_offset,
                "tanScale": self.tan_scale,
                "offset": self.offset,
                "scale": self.scale,
            }
        )


@dataclass(order=True, frozen=True, slots=True)
class ChannelMix(PayloadObject):
    """Channel Mix.

    Mixes both channels (left and right), with a configurable factor on how much each channel affects the other.
    With the defaults, both channels are kept independent of each other. Setting all factors to 0.5 means both channels get the same audio.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#channel-mix)
    """

    left_to_left: float | None
    """The left to left channel mix factor (0.0 ≤ x ≤ 1.0)."""

    left_to_right: float | None
    """The left to right channel mix factor (0.0 ≤ x ≤ 1.0)."""

    right_to_left: float | None
    """The right to left channel mix factor (0.0 ≤ x ≤ 1.0)."""

    right_to_right: float | None
    """The right to right channel mix factor (0.0 ≤ x ≤ 1.0)."""

    def __post_init__(self) -> None:
        if self.left_to_left is not None and (
            self.left_to_left > 1 or self.left_to_left < 0
        ):
            raise ValueError("Left to Left must be in range (0; 1).")

        if self.left_to_right is not None and (
            self.left_to_right > 1 or self.left_to_right < 0
        ):
            raise ValueError("Left to Right must be in range (0; 1).")

        if self.right_to_left is not None and (
            self.right_to_left > 1 or self.right_to_left < 0
        ):
            raise ValueError("Right to Left must be in range (0; 1).")

        if self.right_to_right is not None and (
            self.right_to_right > 1 or self.right_to_right < 0
        ):
            raise ValueError("Right to Right must be in range (0; 1).")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "ChannelMix":
        """Build channel mix filter from payload."""
        return ChannelMix(
            payload.get("leftToLeft", None),
            payload.get("leftToRight", None),
            payload.get("rightToLeft", None),
            payload.get("rightToRight", None),
        )

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload(
            {
                "leftToLeft": self.left_to_left,
                "leftToRight": self.left_to_right,
                "rightToLeft": self.right_to_left,
                "rightToRight": self.right_to_right,
            }
        )


@dataclass(order=True, frozen=True, slots=True)
class LowPass(PayloadObject):
    """Low Pass.

    Higher frequencies get suppressed, while lower frequencies pass through this filter, thus the name low pass.
    Any smoothing values equal to or less than 1.0 will disable the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#low-pass)
    """

    smoothing: float | None
    """The smoothing factor (1.0 < x)."""

    def __post_init__(self) -> None:
        if self.smoothing is not None and self.smoothing < 1:
            raise ValueError("Frequency must be at or above 1.")

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "LowPass":
        """Build low pass filter from payload."""
        return LowPass(payload.get("smoothing", None))

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use it in rest."""
        return _clear_payload({"smoothing": self.smoothing})


@dataclass(order=True, slots=True)
class Filters(PayloadObject):
    """The base class for filter.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#filters)

    To disable filter use:
    ```py
    filters.rotation = None
    ```

    To set filter use:
    ```py
    filter.volume = 10

    filter.karaoke = Karaoke(level=0.5)
    ```
    """

    volume: float | None = None
    """The volume of the player."""

    equalizer: typing.MutableSequence[Equalizer] | None = None
    """15 bands with different gains."""

    karaoke: Karaoke | None = None
    """Eliminates part of a band, usually targeting vocals."""

    timescale: Timescale | None = None
    """The speed, pitch, and rate."""

    tremolo: Tremolo | None = None
    """Creates a shuddering effect, where the volume quickly oscillates."""

    vibrato: Vibrato | None = None
    """Creates a shuddering effect, where the pitch quickly oscillates."""

    rotation: Rotation | None = None
    """Rotates the audio around the stereo channels/user headphones (aka Audio Panning)."""

    distortion: Distortion | None = None
    """Distorts the audio."""

    channel_mix: ChannelMix | None = None
    """Mixes both channels (left and right)."""

    low_pass: LowPass | None = None
    """Filters higher frequencies."""

    plugin_filters: typing.MutableMapping[str, typing.Any] | None = None
    """Filter plugin configurations."""

    def set_volume(self, volume: float) -> Self:
        """Set the volume of the filter.

        Parameters
        ----------
        volume
            The volume of the player (Must be greater than 0).
        """
        if volume <= 0:
            raise ValueError("Volume must be at or above 0.")
        self.volume = volume
        return self

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Filters":
        equalizer: list[Equalizer] = []
        if payload.get("equalizer", None) is not None:
            for eq in payload["equalizer"]:
                equalizer.append(Equalizer.from_payload(eq))

        return Filters(
            volume=payload.get("volume", None),
            equalizer=equalizer,
            karaoke=Karaoke.from_payload(payload["karaoke"])
            if payload.get("karaoke", None)
            else None,
            timescale=Timescale.from_payload(payload["timescale"])
            if payload.get("timescale", None)
            else None,
            tremolo=Tremolo.from_payload(payload["tremolo"])
            if payload.get("tremolo", None)
            else None,
            vibrato=Vibrato.from_payload(payload["vibrato"])
            if payload.get("vibrato", None)
            else None,
            rotation=Rotation.from_payload(payload["rotation"])
            if payload.get("rotation", None)
            else None,
            distortion=Distortion.from_payload(payload["distortion"])
            if payload.get("distortion", None)
            else None,
            channel_mix=ChannelMix.from_payload(payload["channelMix"])
            if payload.get("channelMix", None)
            else None,
            low_pass=LowPass.from_payload(payload["lowPass"])
            if payload.get("lowPass", None)
            else None,
            plugin_filters=payload.get("pluginFilters", None),
        )

    def add_equalizer(self, band: BandType, gain: float) -> Self:
        """Add a new equalizer band, with appropriate gain.

        Parameters
        ----------
        band
            The [BandType][ongaku.abc.filters.BandType].
        gain
            The gain of the band. (-0.25 to 1.0)
        """
        if self.equalizer is None:
            self.equalizer = [Equalizer(band, gain)]
        else:
            self.equalizer.append(Equalizer(band, gain))

        return self

    def remove_equalizer(self, band: BandType) -> Self:
        """Remove a equalizer via its band.

        Parameters
        ----------
        band
            The [BandType][ongaku.abc.filters.BandType].
        """
        if self.equalizer is None:
            raise ValueError("Equalizer is None")

        for equalizer in self.equalizer:
            if equalizer.band == band:
                self.equalizer.remove(equalizer)
                return self

        raise IndexError("No values found.")

    def dump(self) -> dict[str, typing.Any] | None:
        """Dump filter to use in rest."""
        res = {
            "volume": self.volume,
            "equalizer": [eq.dump() for eq in self.equalizer or []],
            "pluginFilter": self.plugin_filters,
        }

        filters = (
            ("karaoke", self.karaoke),
            ("timescale", self.timescale),
            ("tremolo", self.tremolo),
            ("vibrate", self.vibrato),
            ("rotation", self.rotation),
            ("distortion", self.distortion),
            ("channelMix", self.channel_mix),
            ("lowPass", self.low_pass),
        )
        for name, attr in filters:
            if attr is None:
                continue
            dump = attr.dump()
            if dump is not None:
                res[name] = dump

        return _clear_payload(res)
