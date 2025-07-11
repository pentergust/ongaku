import pytest

from ongaku.impl.filters import BandType
from ongaku.impl.filters import ChannelMix
from ongaku.impl.filters import Distortion
from ongaku.impl.filters import Equalizer
from ongaku.impl.filters import Filters
from ongaku.impl.filters import Karaoke
from ongaku.impl.filters import LowPass
from ongaku.impl.filters import Rotation
from ongaku.impl.filters import Timescale
from ongaku.impl.filters import Tremolo
from ongaku.impl.filters import Vibrato


def test_filters():
    equalizer = [
        Equalizer(BandType.HZ100, 0.95),
        Equalizer(BandType.HZ63, -0.1),
    ]
    karaoke = Karaoke(1, 0.5, 4.5, 6)
    timescale = Timescale(1.2, 2.3, 4)
    tremolo = Tremolo(1.2, 1)
    vibrato = Vibrato(3, 0.5)
    rotation = Rotation(6)
    distortion = Distortion(2.1, 3, 6.9, 7.2, 9.4, 2, 4.1, 8)
    channel_mix = ChannelMix(0, 1, 0.5, 0.63)
    low_pass = LowPass(3.8)
    filters = Filters(
        volume=1.2,
        equalizer=equalizer,
        karaoke=karaoke,
        timescale=timescale,
        tremolo=tremolo,
        vibrato=vibrato,
        rotation=rotation,
        distortion=distortion,
        channel_mix=channel_mix,
        low_pass=low_pass,
    )

    assert filters.volume == 1.2
    assert filters.equalizer == equalizer
    assert filters.karaoke == karaoke
    assert filters.timescale == timescale
    assert filters.tremolo == tremolo
    assert filters.vibrato == vibrato
    assert filters.rotation == rotation
    assert filters.distortion == distortion
    assert filters.channel_mix == channel_mix
    assert filters.low_pass == low_pass
    assert filters.plugin_filters is None


class TestFilterFunctions:
    def test_from_filter(self, ongaku_filters: Filters):
        filters = ongaku_filters

        assert filters.volume == 1.2
        assert filters.equalizer == ongaku_filters.equalizer
        assert filters.karaoke == ongaku_filters.karaoke
        assert filters.timescale == ongaku_filters.timescale
        assert filters.tremolo == ongaku_filters.tremolo
        assert filters.vibrato == ongaku_filters.vibrato
        assert filters.rotation == ongaku_filters.rotation
        assert filters.distortion == ongaku_filters.distortion
        assert filters.channel_mix == ongaku_filters.channel_mix
        assert filters.low_pass == ongaku_filters.low_pass
        assert filters.plugin_filters is None

    def test_set_volume(self):
        filters = Filters()

        filters.set_volume(10)
        assert filters.volume == 10

        with pytest.raises(ValueError):
            filters.set_volume(-0.1)

    def test_add_equalizer(self):
        filters = Filters()
        filters.equalizer = [Equalizer(BandType.HZ100, 0.3)]

        assert len(filters.equalizer) == 1
        assert filters.equalizer[0].band == BandType.HZ100
        assert filters.equalizer[0].gain == 0.3

    def test_remove_equalizer(self):
        filters = Filters()

        filters.add_equalizer(BandType.HZ100, 0.3)
        assert filters.equalizer is not None
        assert len(filters.equalizer) == 1

        filters.remove_equalizer(BandType.HZ100)
        assert len(filters.equalizer) == 0

        with pytest.raises(IndexError):
            filters.remove_equalizer(BandType.HZ100)

    def test_clear_equalizer(self):
        filters = Filters()

        filters.add_equalizer(BandType.HZ100, 0.3)
        filters.add_equalizer(BandType.HZ630, 0.5)

        assert filters.equalizer is not None
        assert len(filters.equalizer) == 2

        filters.equalizer = None
        assert filters.equalizer is None

    def test_set_karaoke(self):
        filters = Filters()

        filters.karaoke = Karaoke(
            level=0.1, mono_level=1.0, filter_band=0.5, filter_width=2
        )

        assert filters.karaoke is not None
        assert filters.karaoke.level == 0.1
        assert filters.karaoke.mono_level == 1.0
        assert filters.karaoke.filter_band == 0.5
        assert filters.karaoke.filter_width == 2

    def test_clear_karaoke(self):
        filters = Filters()
        filters.karaoke = Karaoke(
            level=0.1, mono_level=1.0, filter_band=0.5, filter_width=2
        )

        assert filters.karaoke is not None

        filters.karaoke = None
        assert filters.karaoke is None

    def test_set_timescale(self):
        filters = Filters()
        filters.timescale = Timescale(speed=1, pitch=0.5, rate=0.66)

        assert filters.timescale is not None
        assert filters.timescale.speed == 1
        assert filters.timescale.pitch == 0.5
        assert filters.timescale.rate == 0.66

    def test_clear_timescale(self):
        filters = Filters()
        filters.timescale = Timescale(speed=1, pitch=0.5, rate=0.66)
        assert filters.timescale is not None

        filters.timescale = None
        assert filters.timescale is None

    def test_set_tremolo(self):
        filters = Filters()
        filters.tremolo = Tremolo(frequency=8, depth=1)

        assert filters.tremolo is not None
        assert filters.tremolo.frequency == 8
        assert filters.tremolo.depth == 1

    def test_clear_tremolo(self):
        filters = Filters()

        filters.tremolo = Tremolo(frequency=8, depth=1)
        assert filters.tremolo is not None

        filters.tremolo = None
        assert filters.tremolo is None

    def test_set_vibrato(self):
        filters = Filters()
        filters.vibrato = Vibrato(frequency=8, depth=1)

        assert filters.vibrato is not None
        assert filters.vibrato.frequency == 8
        assert filters.vibrato.depth == 1

    def test_clear_vibrato(self):
        filters = Filters()

        filters.vibrato = Vibrato(frequency=8, depth=1)
        assert filters.vibrato is not None

        filters.vibrato = None
        assert filters.vibrato is None

    def test_set_rotation(self):
        filters = Filters()
        filters.rotation = Rotation(rotation_hz=8)

        assert filters.rotation is not None
        assert filters.rotation.rotation_hz == 8

    def test_clear_rotation(self):
        filters = Filters()

        filters.rotation = Rotation(rotation_hz=8)
        assert filters.rotation is not None

        filters.rotation = None
        assert filters.rotation is None

    def test_set_distortion(self):
        filters = Filters()

        filters.distortion = Distortion(
            sin_offset=0.3,
            sin_scale=1,
            cos_offset=4,
            cos_scale=-3,
            tan_offset=4,
            tan_scale=9,
            offset=6.66,
            scale=-1.5,
        )

        assert filters.distortion is not None
        assert filters.distortion.sin_offset == 0.3
        assert filters.distortion.sin_scale == 1
        assert filters.distortion.cos_offset == 4
        assert filters.distortion.cos_scale == -3
        assert filters.distortion.tan_offset == 4
        assert filters.distortion.tan_scale == 9
        assert filters.distortion.offset == 6.66
        assert filters.distortion.scale == -1.5

    def test_clear_distortion(self):
        filters = Filters()

        filters.distortion = Distortion(
            sin_offset=0.3,
            sin_scale=1,
            cos_offset=4,
            cos_scale=-3,
            tan_offset=4,
            tan_scale=9,
            offset=6.66,
            scale=-1.5,
        )

        assert filters.distortion is not None

        filters.distortion = None
        assert filters.distortion is None

    def test_set_channel_mix(self):
        filters = Filters()

        filters.channel_mix = ChannelMix(
            left_to_left=0.39,
            left_to_right=1,
            right_to_left=0,
            right_to_right=0.8,
        )

        assert filters.channel_mix is not None
        assert filters.channel_mix.left_to_left == 0.39
        assert filters.channel_mix.left_to_right == 1
        assert filters.channel_mix.right_to_left == 0
        assert filters.channel_mix.right_to_right == 0.8

    def test_clear_channel_mix(self):
        filters = Filters()

        filters.channel_mix = ChannelMix(
            left_to_left=0.39,
            left_to_right=1,
            right_to_left=0,
            right_to_right=0.8,
        )

        assert filters.channel_mix is not None

        filters.channel_mix = None
        assert filters.channel_mix is None

    def test_set_low_pass(self):
        filters = Filters()

        filters.low_pass = LowPass(smoothing=8)
        assert filters.low_pass is not None
        assert filters.low_pass.smoothing == 8

    def test_clear_low_pass(self):
        filters = Filters()

        filters.low_pass = LowPass(smoothing=8)
        assert filters.low_pass is not None

        filters.low_pass = None
        assert filters.low_pass is None

    def test_set_plugin_filters(self):
        filters = Filters()
        payload = {"beanos": "beanos"}
        filters.plugin_filters = payload
        assert filters.plugin_filters == payload


class TestEqualizer:
    def test_valid_values(self):
        equalizer = Equalizer(BandType.HZ100, 0.5)

        assert equalizer.band == BandType.HZ100
        assert equalizer.gain == 0.5

    def test_invalid_positive_gain_value(self):
        with pytest.raises(ValueError):
            Equalizer(BandType.HZ100, 1.1)

    def test_invalid_negative_gain_value(self):
        with pytest.raises(ValueError):
            Equalizer(BandType.HZ100, -0.26)


class TestKaraoke:
    def test_valid_values(self):
        karaoke = Karaoke(1, 0.65, 4.5, 6)

        assert karaoke.level == 1
        assert karaoke.mono_level == 0.65
        assert karaoke.filter_band == 4.5
        assert karaoke.filter_width == 6

    def test_invalid_negative_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(-0.1, 0.65, 4.5, 6)

    def test_invalid_positive_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(1.1, 0.65, 4.5, 6)

    def test_invalid_negative_mono_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(1, -0.1, 4.5, 6)

    def test_invalid_positive_mono_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(1, 1.1, 4.5, 6)


class TestTimescale:
    def test_valid_values(self):
        timescale = Timescale(1.2, 2.3, 4)

        assert timescale.speed == 1.2
        assert timescale.pitch == 2.3
        assert timescale.rate == 4

    def test_invalid_negative_speed_value(self):
        with pytest.raises(ValueError):
            Timescale(-0.1, 2.3, 4)

    def test_invalid_negative_pitch_value(self):
        with pytest.raises(ValueError):
            Timescale(1.2, -0.1, 4)

    def test_invalid_negative_rate_value(self):
        with pytest.raises(ValueError):
            Timescale(1.2, 2.3, -0.1)


class TestTremolo:
    def test_valid_values(self):
        tremolo = Tremolo(1.2, 1)

        assert tremolo.frequency == 1.2
        assert tremolo.depth == 1

    def test_invalid_negative_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(-0.1, 1)

    def test_invalid_negative_depth_value(self):
        with pytest.raises(ValueError):
            Tremolo(1.2, -0.1)

    def test_invalid_positive_depth_value(self):
        with pytest.raises(ValueError):
            Tremolo(1.2, 1.1)


class TestVibrato:
    def test_valid_values(self):
        vibrato = Vibrato(3, 0.5)

        assert vibrato.frequency == 3
        assert vibrato.depth == 0.5

    def test_invalid_negative_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(-0.1, 0.5)

    def test_invalid_positive_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(14.1, 1.1)

    def test_invalid_negative_depth_value(self):
        with pytest.raises(ValueError):
            Vibrato(3, -0.1)

    def test_invalid_positive_depth_value(self):
        with pytest.raises(ValueError):
            Vibrato(3, 1.1)


def test_rotation():
    rotation = Rotation(6)

    assert rotation.rotation_hz == 6


def test_distortion():
    distortion = Distortion(2.1, 3, 6.9, 7.2, 9.4, 2, 4.1, 8)

    assert distortion.sin_offset == 2.1
    assert distortion.sin_scale == 3
    assert distortion.cos_offset == 6.9
    assert distortion.cos_scale == 7.2
    assert distortion.tan_offset == 9.4
    assert distortion.tan_scale == 2
    assert distortion.offset == 4.1
    assert distortion.scale == 8


class TestChannelMix:
    def test_valid_values(self):
        channel_mix = ChannelMix(0, 1, 0.5, 0.63)

        assert channel_mix.left_to_left == 0
        assert channel_mix.left_to_right == 1
        assert channel_mix.right_to_left == 0.5
        assert channel_mix.right_to_right == 0.63

    def test_invalid_negative_left_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(-0.1, 1, 0.5, 0.63)

    def test_invalid_positive_left_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(1.1, 1, 0.5, 0.63)

    def test_invalid_negative_left_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, -0.1, 0.5, 0.63)

    def test_invalid_positive_left_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1.1, 0.5, 0.63)

    def test_invalid_negative_right_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, -0.1, 0.63)

    def test_invalid_positive_right_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, 1.1, 0.63)

    def test_invalid_negative_right_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, 0.5, -0.1)

    def test_invalid_positive_right_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, 0.5, 1.1)


class TestLowPass:
    def test_valid_values(self):
        low_pass = LowPass(3.8)

        assert low_pass.smoothing == 3.8

    def test_invalid_negative_smoothing_value(self):
        with pytest.raises(ValueError):
            LowPass(0.9)
