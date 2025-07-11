import typing

import hikari
from typing_extensions import Self

from ongaku.abc import filters as filters_


class Filters(filters_.Filters):
    """Filters.

    An empty filter object.

    Parameters
    ----------
    volume
        Volume of the player.
    equalizer
        A sequence of equalizer objects.
    karaoke
        A karaoke object.
    timescale
        A timescale object.
    tremolo
        A tremolo object.
    vibrato
        A vibrato object.
    rotation
        A rotation object.
    distortion
        A distortion object.
    channel_mix
        A channel mix object.
    low_pass
        A low pass object.
    plugin_filters
        A dict of plugin filters.

    """

    def __init__(
        self,
        *,
        volume: float | None = None,
        equalizer: typing.Sequence[filters_.Equalizer] = [],
        karaoke: filters_.Karaoke | None = None,
        timescale: filters_.Timescale | None = None,
        tremolo: filters_.Tremolo | None = None,
        vibrato: filters_.Vibrato | None = None,
        rotation: filters_.Rotation | None = None,
        distortion: filters_.Distortion | None = None,
        channel_mix: filters_.ChannelMix | None = None,
        low_pass: filters_.LowPass | None = None,
        plugin_filters: typing.Mapping[str, typing.Any] = {},
    ) -> None:
        self._volume = volume
        self._equalizer: typing.MutableSequence[filters_.Equalizer] = list(
            equalizer
        )
        self._karaoke = karaoke
        self._timescale = timescale
        self._tremolo = tremolo
        self._vibrato = vibrato
        self._rotation = rotation
        self._distortion = distortion
        self._channel_mix = channel_mix
        self._low_pass = low_pass
        self._plugin_filters = plugin_filters

    @classmethod
    def from_filter(cls, filters: filters_.Filters) -> Self:
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

    def add_equalizer(
        self,
        band: filters_.BandType,
        gain: float,
    ) -> Self:
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

    def remove_equalizer(self, band: filters_.BandType) -> Self:
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


class Equalizer(filters_.Equalizer):
    def __init__(
        self,
        band: filters_.BandType,
        gain: float,
    ) -> None:
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
        return Equalizer(filters_.BandType(payload["band"]), payload["gain"])


class Karaoke(filters_.Karaoke):
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


class Timescale(filters_.Timescale):
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


class Tremolo(filters_.Tremolo):
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


class Vibrato(filters_.Vibrato):
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


class Rotation(filters_.Rotation):
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


class Distortion(filters_.Distortion):
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


class ChannelMix(filters_.ChannelMix):
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


class LowPass(filters_.LowPass):
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
