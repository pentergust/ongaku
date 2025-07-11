import typing
from enum import IntEnum

import hikari
from typing_extensions import Self

from ongaku.impl.payload import PayloadObject

__all__ = ("BandType", "Filters")


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


class Equalizer(PayloadObject):
    """Equalizer.

    There are 15 bands (0-14) that can be changed.
    "gain" is the multiplier for the given band.
    The default value is 0. Valid values range from -0.25 to 1.0,
    where -0.25 means the given band is completely muted, and 0.25 means it is doubled.
    Modifying the gain could also change the volume of the output.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#equalizer)
    """

    __slots__: typing.Sequence[str] = ("_band", "_gain")

    def __init__(self, band: BandType, gain: float) -> None:
        if gain > 1:
            raise ValueError("Gain must be at or below 1.")
        if gain < -0.25:
            raise ValueError("Gain must be at or above -0.25.")

        self._band = band
        self._gain = gain

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Equalizer":
        return Equalizer(BandType(payload["band"]), payload["gain"])

    @property
    def band(self) -> BandType:
        """The band (0 to 14)."""
        return self._band

    @property
    def gain(self) -> float:
        """The gain (-0.25 to 1.0)."""
        return self._gain

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Equalizer):
            return False

        if self.band != other.band:
            return False

        return self.gain == other.gain


class Karaoke(PayloadObject):
    """Karaoke.

    Uses equalization to eliminate part of a band, usually targeting vocals.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#karaoke)
    """

    __slots__: typing.Sequence[str] = (
        "_filter_band",
        "_filter_width",
        "_level",
        "_mono_level",
    )

    def __init__(
        self,
        level: float | None,
        mono_level: float | None,
        filter_band: float | None,
        filter_width: float | None,
    ) -> None:
        if level is not None:
            if level > 1:
                raise ValueError("Level must be at or below 1.")
            if level < 0:
                raise ValueError("Level must be at or above 0.")

        if mono_level is not None:
            if mono_level > 1:
                raise ValueError("MonoLevel must be at or below 1.")
            if mono_level < 0:
                raise ValueError("MonoLevel must be at or above 0.")

        self._level = level
        self._mono_level = mono_level
        self._filter_band = filter_band
        self._filter_width = filter_width

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

    @property
    def level(self) -> float | None:
        """The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
        return self._level

    @property
    def mono_level(self) -> float | None:
        """The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
        return self._mono_level

    @property
    def filter_band(self) -> float | None:
        """The filter band (in Hz)."""
        return self._filter_band

    @property
    def filter_width(self) -> float | None:
        """The filter width."""
        return self._filter_width

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Karaoke):
            return False

        if self.level != other.level:
            return False

        if self.mono_level != other.mono_level:
            return False

        if self.filter_band != other.filter_band:
            return False

        return self.filter_width == other.filter_width


class Timescale(PayloadObject):
    """Timescale.

    Changes the speed, pitch, and rate. All default to 1.0.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#timescale)
    """

    __slots__: typing.Sequence[str] = ("_pitch", "_rate", "_speed")

    def __init__(
        self,
        speed: float | None,
        pitch: float | None,
        rate: float | None,
    ) -> None:
        if speed is not None and speed < 0:
            raise ValueError("Speed must be at or above 0.")
        if pitch is not None and pitch < 0:
            raise ValueError("Pitch must be at or above 0.")
        if rate is not None and rate < 0:
            raise ValueError("Rate must be at or above 0.")

        self._speed = speed
        self._pitch = pitch
        self._rate = rate

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Timescale":
        return Timescale(
            payload.get("speed", None),
            payload.get("pitch", None),
            payload.get("rate", None),
        )

    @property
    def speed(self) -> float | None:
        """The playback speed 0.0 ≤ x."""
        return self._speed

    @property
    def pitch(self) -> float | None:
        """The pitch 0.0 ≤ x."""
        return self._pitch

    @property
    def rate(self) -> float | None:
        """The rate 0.0 ≤ x."""
        return self._rate

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Timescale):
            return False

        if self.speed != other.speed:
            return False

        if self.pitch != other.pitch:
            return False

        return self.rate == other.rate


class Tremolo(PayloadObject):
    """Tremolo.

    Uses amplification to create a shuddering effect, where the volume quickly oscillates.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#tremolo)
    """

    __slots__: typing.Sequence[str] = (
        "_depth",
        "_frequency",
    )

    def __init__(self, frequency: float | None, depth: float | None) -> None:
        if frequency is not None and frequency < 0:
            raise ValueError("Frequency must be at or above 0.")

        if depth is not None:
            if depth > 1:
                raise ValueError("Depth must be at or below 1.")
            if depth < 0:
                raise ValueError("Depth must be at or above 0.")

        self._frequency = frequency
        self._depth = depth

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Tremolo":
        """Build tremolo filter from payload."""
        return Tremolo(
            payload.get("frequency", None),
            payload.get("depth", None),
        )

    @property
    def frequency(self) -> float | None:
        """The frequency 0.0 < x."""
        return self._frequency

    @property
    def depth(self) -> float | None:
        """The tremolo depth 0.0 < x ≤ 1.0."""
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tremolo):
            return False

        if self.frequency != other.frequency:
            return False

        return self.depth == other.depth


class Vibrato(PayloadObject):
    """Vibrato.

    Similar to tremolo. While tremolo oscillates the volume, vibrato oscillates the pitch.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#vibrato)
    """

    __slots__: typing.Sequence[str] = (
        "_depth",
        "_frequency",
    )

    def __init__(self, frequency: float | None, depth: float | None) -> None:
        if frequency is not None:
            if frequency > 14:
                raise ValueError("Frequency must be at or below 1.")
            if frequency < 0:
                raise ValueError("Frequency must be at or above 0.")

        if depth is not None:
            if depth > 1:
                raise ValueError("Depth must be at or below 1.")
            if depth < 0:
                raise ValueError("Depth must be at or above 0.")

        self._frequency = frequency
        self._depth = depth

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Vibrato":
        """Build vibrato filter from payload."""
        return Vibrato(
            payload.get("frequency", None),
            payload.get("depth", None),
        )

    @property
    def frequency(self) -> float | None:
        """The frequency 0.0 < x ≤ 14.0."""
        return self._frequency

    @property
    def depth(self) -> float | None:
        """The vibrato depth 0.0 < x ≤ 1.0."""
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vibrato):
            return False

        if self.frequency != other.frequency:
            return False

        return self.depth == other.depth


class Rotation(PayloadObject):
    """Rotation.

    Rotates the sound around the stereo channels/user headphones (aka Audio Panning).

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#rotation)
    """

    __slots__: typing.Sequence[str] = "_rotation_hz"

    def __init__(self, rotation_hz: float | None) -> None:
        self._rotation_hz = rotation_hz

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "Rotation":
        """Build rotation filter from payload."""
        return Rotation(
            payload.get("rotationHz", None),
        )

    @property
    def rotation_hz(self) -> float | None:
        """The frequency of the audio rotating around the listener in Hz."""
        return self._rotation_hz

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rotation):
            return False

        return self.rotation_hz == other.rotation_hz


class Distortion(PayloadObject):
    """Distortion.

    Distortion effect. It can generate some pretty unique audio effects.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#distortion)
    """

    __slots__: typing.Sequence[str] = (
        "_cos_offset",
        "_cos_scale",
        "_offset",
        "_scale",
        "_sin_offset",
        "_sin_scale",
        "_tan_offset",
        "_tan_scale",
    )

    def __init__(
        self,
        sin_offset: float | None,
        sin_scale: float | None,
        cos_offset: float | None,
        cos_scale: float | None,
        tan_offset: float | None,
        tan_scale: float | None,
        offset: float | None,
        scale: float | None,
    ) -> None:
        self._sin_offset = sin_offset
        self._sin_scale = sin_scale
        self._cos_offset = cos_offset
        self._cos_scale = cos_scale
        self._tan_offset = tan_offset
        self._tan_scale = tan_scale
        self._offset = offset
        self._scale = scale

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

    @property
    def sin_offset(self) -> float | None:
        """The sin offset."""
        return self._sin_offset

    @property
    def sin_scale(self) -> float | None:
        """The sin scale."""
        return self._sin_scale

    @property
    def cos_offset(self) -> float | None:
        """The cos offset."""
        return self._cos_offset

    @property
    def cos_scale(self) -> float | None:
        """The cos scale."""
        return self._cos_scale

    @property
    def tan_offset(self) -> float | None:
        """The tan offset."""
        return self._tan_offset

    @property
    def tan_scale(self) -> float | None:
        """The tan scale."""
        return self._tan_scale

    @property
    def offset(self) -> float | None:
        """The offset."""
        return self._offset

    @property
    def scale(self) -> float | None:
        """The scale."""
        return self._scale

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Distortion):
            return False

        if self.sin_offset != other.sin_offset:
            return False

        if self.sin_scale != other.sin_scale:
            return False

        if self.cos_offset != other.cos_offset:
            return False

        if self.cos_scale != other.cos_scale:
            return False

        if self.tan_offset != other.tan_offset:
            return False

        if self.tan_scale != other.tan_scale:
            return False

        if self.offset != other.offset:
            return False

        return self.scale == other.scale


class ChannelMix(PayloadObject):
    """Channel Mix.

    Mixes both channels (left and right), with a configurable factor on how much each channel affects the other.
    With the defaults, both channels are kept independent of each other. Setting all factors to 0.5 means both channels get the same audio.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#channel-mix)
    """

    __slots__: typing.Sequence[str] = (
        "_left_to_left",
        "_left_to_right",
        "_right_to_left",
        "_right_to_right",
    )

    def __init__(  # noqa: C901
        self,
        left_to_left: float | None,
        left_to_right: float | None,
        right_to_left: float | None,
        right_to_right: float | None,
    ) -> None:
        if left_to_left is not None:
            if left_to_left > 1:
                raise ValueError("Left to Left must be at or below 1.")
            if left_to_left < 0:
                raise ValueError("Left to Left must be at or above 0.")

        if left_to_right is not None:
            if left_to_right > 1:
                raise ValueError("Left to Right must be at or below 1.")
            if left_to_right < 0:
                raise ValueError("Left to Right must be at or above 0.")

        if right_to_left is not None:
            if right_to_left > 1:
                raise ValueError("Right to Left must be at or below 1.")
            if right_to_left < 0:
                raise ValueError("Right to Left must be at or above 0.")

        if right_to_right is not None:
            if right_to_right > 1:
                raise ValueError("Right to Left must be at or below 1.")
            if right_to_right < 0:
                raise ValueError("Right to Left must be at or above 0.")

        self._left_to_left = left_to_left
        self._left_to_right = left_to_right
        self._right_to_left = right_to_left
        self._right_to_right = right_to_right

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

    @property
    def left_to_left(self) -> float | None:
        """The left to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._left_to_left

    @property
    def left_to_right(self) -> float | None:
        """The left to right channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._left_to_right

    @property
    def right_to_left(self) -> float | None:
        """The right to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._right_to_left

    @property
    def right_to_right(self) -> float | None:
        """The right to right channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._right_to_right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChannelMix):
            return False

        if self.left_to_left != other.left_to_left:
            return False

        if self.left_to_right != other.left_to_right:
            return False

        if self.right_to_left != other.right_to_left:
            return False

        return self.right_to_right == other.right_to_right


class LowPass(PayloadObject):
    """Low Pass.

    Higher frequencies get suppressed, while lower frequencies pass through this filter, thus the name low pass.
    Any smoothing values equal to or less than 1.0 will disable the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#low-pass)
    """

    __slots__: typing.Sequence[str] = ("_smoothing",)

    def __init__(
        self,
        smoothing: float | None,
    ) -> None:
        if smoothing is not None and smoothing < 1:
            raise ValueError("Frequency must be at or above 1.")

        self._smoothing = smoothing

    @classmethod
    def _from_payload(
        cls, payload: typing.Mapping[str, typing.Any]
    ) -> "LowPass":
        """Build low pass filter from payload."""
        return LowPass(
            payload.get("smoothing", None),
        )

    @property
    def smoothing(self) -> float | None:
        """The smoothing factor (1.0 < x)."""
        return self._smoothing

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LowPass):
            return False

        return self.smoothing == other.smoothing


class Filters(PayloadObject):
    """Filters.

    The base class for filter.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#filters)
    """

    __slots__: typing.Sequence[str] = (
        "_channel_mix",
        "_distortion",
        "_equalizer",
        "_karaoke",
        "_low_pass",
        "_plugin_filters",
        "_rotation",
        "_timescale",
        "_tremolo",
        "_vibrato",
        "_volume",
    )

    def __init__(
        self,
        *,
        volume: float | None = None,
        equalizer: typing.Sequence[Equalizer] = [],
        karaoke: Karaoke | None = None,
        timescale: Timescale | None = None,
        tremolo: Tremolo | None = None,
        vibrato: Vibrato | None = None,
        rotation: Rotation | None = None,
        distortion: Distortion | None = None,
        channel_mix: ChannelMix | None = None,
        low_pass: LowPass | None = None,
        plugin_filters: typing.Mapping[str, typing.Any] = {},
    ) -> None:
        self._volume = volume
        self._equalizer: typing.MutableSequence[Equalizer] = list(equalizer)
        self._karaoke = karaoke
        self._timescale = timescale
        self._tremolo = tremolo
        self._vibrato = vibrato
        self._rotation = rotation
        self._distortion = distortion
        self._channel_mix = channel_mix
        self._low_pass = low_pass
        self._plugin_filters = plugin_filters

    @property
    def volume(self) -> float | None:
        """Volume.

        The volume of the player.
        """
        return self._volume

    @property
    def equalizer(self) -> typing.Sequence[Equalizer]:
        """Equalizer.

        15 bands with different gains.
        """
        return self._equalizer

    @property
    def karaoke(self) -> Karaoke | None:
        """Karaoke.

        Eliminates part of a band, usually targeting vocals.
        """
        return self._karaoke

    @property
    def timescale(self) -> Timescale | None:
        """Timescale.

        The speed, pitch, and rate.
        """
        return self._timescale

    @property
    def tremolo(self) -> Tremolo | None:
        """Tremolo.

        Creates a shuddering effect, where the volume quickly oscillates.
        """
        return self._tremolo

    @property
    def vibrato(self) -> Vibrato | None:
        """Vibrato.

        Creates a shuddering effect, where the pitch quickly oscillates.
        """
        return self._vibrato

    @property
    def rotation(self) -> Rotation | None:
        """Rotation.

        Rotates the audio around the stereo channels/user headphones (aka Audio Panning).
        """
        return self._rotation

    @property
    def distortion(self) -> Distortion | None:
        """Distortion.

        Distorts the audio.
        """
        return self._distortion

    @property
    def channel_mix(self) -> ChannelMix | None:
        """Channel Mix.

        Mixes both channels (left and right).
        """
        return self._channel_mix

    @property
    def low_pass(self) -> LowPass | None:
        """Low Pass.

        Filters higher frequencies.
        """
        return self._low_pass

    @property
    def plugin_filters(self) -> typing.Mapping[str, typing.Any]:
        """Plugin Filters.

        Filter plugin configurations.
        """
        return self._plugin_filters

    def __eq__(self, other: object) -> bool:  # noqa: C901
        if not isinstance(other, Filters):
            return False

        if self.volume != other.volume:
            return False

        if self.equalizer != other.equalizer:
            return False

        if self.karaoke != other.karaoke:
            return False

        if self.timescale != other.timescale:
            return False

        if self.tremolo != other.tremolo:
            return False

        if self.vibrato != other.vibrato:
            return False

        if self.rotation != other.rotation:
            return False

        if self.distortion != other.distortion:
            return False

        if self.channel_mix != other.channel_mix:
            return False

        if self.low_pass != other.low_pass:
            return False

        return self.plugin_filters == other.plugin_filters

    @classmethod
    def from_filter(cls, filters: Self) -> Self:
        """From Filter.

        Convert a immutable filter, into a mutable filter.

        !!! note
            The purpose of this is so that you can modify a players filter object, without directly modifying it.

        Parameters
        ----------
        filters
            The filter to pull data from.
        """
        return cls(
            volume=filters.volume,
            equalizer=filters.equalizer,
            karaoke=filters.karaoke,
            timescale=filters.timescale,
            tremolo=filters.tremolo,
            vibrato=filters.vibrato,
            rotation=filters.rotation,
            distortion=filters.distortion,
            channel_mix=filters.channel_mix,
            low_pass=filters.low_pass,
        )

    def set_volume(self, volume: float) -> Self:
        """Set Volume.

        Set the volume of the filter.

        Parameters
        ----------
        volume
            The volume of the player. (Must be greater than 0.)
        """
        if volume <= 0:
            raise ValueError("Volume must be at or above 0.")
        self._volume = volume

        return self

    # Equalizer

    def add_equalizer(self, band: BandType, gain: float) -> Self:
        """Add Equalizer.

        Add a new equalizer band, with appropriate gain.

        Parameters
        ----------
        band
            The [BandType][ongaku.abc.filters.BandType].
        gain
            The gain of the band. (-0.25 to 1.0)
        """
        self._equalizer.append(Equalizer(band, gain))

        return self

    def remove_equalizer(self, band: BandType) -> Self:
        """Remove Equalizer.

        Remove a equalizer via its band.

        Parameters
        ----------
        band
            The [BandType][ongaku.abc.filters.BandType].
        """
        for equalizer in self.equalizer:
            if equalizer.band == band:
                self._equalizer.remove(equalizer)
                return self

        raise IndexError("No values found.")

    def clear_equalizer(self) -> Self:
        """Clear Equalizer.

        Clear all equalizer bands from the filter.
        """
        self._equalizer.clear()

        return self

    # Karaoke

    def set_karaoke(
        self,
        *,
        level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        mono_level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_band: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_width: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Karaoke.

        Set karaoke values.

        Parameters
        ----------
        level
            The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect).
        mono_level
            The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect).
        filter_band
            The filter band (in Hz).
        filter_width
            The filter width.
        """
        if self._karaoke is None:
            self._karaoke = Karaoke(None, None, None, None)

        self._karaoke = Karaoke(
            self._karaoke.level if level == hikari.UNDEFINED else level,
            self._karaoke.mono_level
            if mono_level == hikari.UNDEFINED
            else mono_level,
            self._karaoke.filter_band
            if filter_band == hikari.UNDEFINED
            else filter_band,
            self._karaoke.filter_width
            if filter_width == hikari.UNDEFINED
            else filter_width,
        )

        return self

    def clear_karaoke(self) -> Self:
        """Clear Karaoke.

        Clear all karaoke values from the filter.
        """
        self._karaoke = None
        return self

    # Timescale

    def set_timescale(
        self,
        *,
        speed: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        pitch: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        rate: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Timescale.

        Set timescale values.

        Parameters
        ----------
        speed
            The playback speed 0.0 ≤ x.
        pitch
            The pitch 0.0 ≤ x.
        rate
            The rate 0.0 ≤ x.
        """
        if self._timescale is None:
            self._timescale = Timescale(None, None, None)

        self._timescale = Timescale(
            self._timescale.speed if speed == hikari.UNDEFINED else speed,
            self._timescale.pitch if pitch == hikari.UNDEFINED else pitch,
            self._timescale.rate if rate == hikari.UNDEFINED else rate,
        )

        return self

    def clear_timescale(self) -> Self:
        """Clear Timescale.

        Clear all timescale values from the filter.
        """
        self._timescale = None
        return self

    # Tremolo

    def set_tremolo(
        self,
        *,
        frequency: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        depth: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Tremolo.

        Set tremolo values.

        Parameters
        ----------
        frequency
            The frequency 0.0 < x.
        depth
            The tremolo depth 0.0 < x ≤ 1.0.
        """
        if self._tremolo is None:
            self._tremolo = Tremolo(None, None)

        self._tremolo = Tremolo(
            self._tremolo.frequency
            if frequency == hikari.UNDEFINED
            else frequency,
            self._tremolo.depth if depth == hikari.UNDEFINED else depth,
        )

        return self

    def clear_tremolo(self) -> Self:
        """Clear Tremolo.

        Clear all tremolo values from the filter.
        """
        self._tremolo = None
        return self

    # Vibrato

    def set_vibrato(
        self,
        *,
        frequency: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        depth: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Vibrato.

        Set vibrato values.

        Parameters
        ----------
        frequency
            The frequency 0.0 < x ≤ 14.0.
        depth
            The vibrato depth 0.0 < x ≤ 1.0.

        """
        if self._vibrato is None:
            self._vibrato = Vibrato(None, None)

        self._vibrato = Vibrato(
            self._vibrato.frequency
            if frequency == hikari.UNDEFINED
            else frequency,
            self._vibrato.depth if depth == hikari.UNDEFINED else depth,
        )

        return self

    def clear_vibrato(self) -> Self:
        """Clear Vibrato.

        Clear all vibrato values from the filter.
        """
        self._vibrato = None
        return self

    # Rotation

    def set_rotation(
        self,
        *,
        rotation_hz: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Rotation.

        Set rotation values.

        Parameters
        ----------
        rotation_hz
            The frequency of the audio rotating around the listener in Hz.
        """
        if self._rotation is None:
            self._rotation = Rotation(None)

        self._rotation = Rotation(
            self._rotation.rotation_hz
            if rotation_hz == hikari.UNDEFINED
            else rotation_hz,
        )

        return self

    def clear_rotation(self) -> Self:
        """Clear Rotation.

        Clear all rotation values from the filter.
        """
        self._rotation = None
        return self

    # Distortion

    def set_distortion(
        self,
        *,
        sin_offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        sin_scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        cos_offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        cos_scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        tan_offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        tan_scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Distortion.

        Set distortion values.

        Parameters
        ----------
        sin_offset
            The sin offset.
        sin_scale
            The sin scale.
        cos_offset
            The cos offset.
        cos_scale
            The cos scale.
        tan_offset
            The tan offset.
        tan_scale
            The tan scale.
        offset
            The offset.
        scale
            The scale.
        """
        if self._distortion is None:
            self._distortion = Distortion(
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )

        self._distortion = Distortion(
            self._distortion.sin_offset
            if sin_offset == hikari.UNDEFINED
            else sin_offset,
            self._distortion.sin_scale
            if sin_scale == hikari.UNDEFINED
            else sin_scale,
            self._distortion.cos_offset
            if cos_offset == hikari.UNDEFINED
            else cos_offset,
            self._distortion.cos_scale
            if cos_scale == hikari.UNDEFINED
            else cos_scale,
            self._distortion.tan_offset
            if tan_offset == hikari.UNDEFINED
            else tan_offset,
            self._distortion.tan_scale
            if tan_scale == hikari.UNDEFINED
            else tan_scale,
            self._distortion.offset if offset == hikari.UNDEFINED else offset,
            self._distortion.scale if scale == hikari.UNDEFINED else scale,
        )

        return self

    def clear_distortion(self) -> Self:
        """Clear Distortion.

        Clear all distortion values from the filter.
        """
        self._distortion = None
        return self

    # Channel Mix

    def set_channel_mix(
        self,
        *,
        left_to_left: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        left_to_right: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        right_to_left: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        right_to_right: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Channel Mix.

        Set tremolo values.

        Parameters
        ----------
        left_to_left
            The left to left channel mix factor (0.0 ≤ x ≤ 1.0).
        left_to_right
            The left to right channel mix factor (0.0 ≤ x ≤ 1.0).
        right_to_left
            The right to left channel mix factor (0.0 ≤ x ≤ 1.0).
        right_to_right
            The right to right channel mix factor (0.0 ≤ x ≤ 1.0).

        """
        if self._channel_mix is None:
            self._channel_mix = ChannelMix(None, None, None, None)

        self._channel_mix = ChannelMix(
            self._channel_mix.left_to_left
            if left_to_left == hikari.UNDEFINED
            else left_to_left,
            self._channel_mix.left_to_right
            if left_to_right == hikari.UNDEFINED
            else left_to_right,
            self._channel_mix.right_to_left
            if right_to_left == hikari.UNDEFINED
            else right_to_left,
            self._channel_mix.right_to_right
            if right_to_right == hikari.UNDEFINED
            else right_to_right,
        )

        return self

    def clear_channel_mix(self) -> Self:
        """Clear Channel Mix.

        Clear all channel mix values from the filter.
        """
        self._channel_mix = None
        return self

    # Low Pass

    def set_low_pass(
        self,
        *,
        smoothing: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Self:
        """Set Low Pass.

        Set low pass values.

        Parameters
        ----------
        smoothing
            The smoothing factor (1.0 < x).
        """
        if self._low_pass is None:
            self._low_pass = LowPass(None)

        self._low_pass = LowPass(
            self._low_pass.smoothing
            if smoothing == hikari.UNDEFINED
            else smoothing,
        )

        return self

    def clear_low_pass(self) -> Self:
        """Clear Low Pass.

        Clear all low pass values from the filter.
        """
        self._low_pass = None
        return self

    # Plugin filters

    def set_plugin_filters(
        self,
        plugin_filters: typing.Mapping[str, typing.Any] = {},
    ) -> Self:
        """Set Plugin Filters.

        Set the filters for plugins.

        Parameters
        ----------
        plugin_filters
            The plugin filters you wish to set.
        """
        self._plugin_filters = plugin_filters
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
