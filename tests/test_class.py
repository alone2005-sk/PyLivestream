#!/usr/bin/env python
from pathlib import Path
import pylivestream as pls
import pytest
from pytest import approx

R = Path(__file__).parent
VIDFN = R / 'bunny.avi'


def test_key():
    """tests reading of stream key"""
    assert pls.utils.getstreamkey('abc123') == 'abc123'
    assert pls.utils.getstreamkey(R / 'periscope.key') == 'abcd1234'


@pytest.mark.parametrize('key', ['', None], ids=['empty string', 'None'])
def test_empty_key(key):
    assert pls.utils.getstreamkey(key) is None


@pytest.mark.parametrize('key', [R, R/'nothere.key'])
def test_bad_key(key):

    with pytest.raises(FileNotFoundError):
        assert pls.utils.getstreamkey(key) is None


@pytest.mark.parametrize('rex', (None, '', 'ffmpeg'))
def test_exe(rex):
    exe, pexe = pls.utils.getexe()
    assert 'ffmpeg' in exe
    assert 'ffprobe' in pexe

    exe, pexe = pls.utils.getexe(rex)
    assert 'ffmpeg' in exe
    assert 'ffprobe' in pexe


@pytest.mark.parametrize('inp', (None, ''))
def test_attrs(inp):
    assert pls.utils.get_resolution(inp) is None

    assert pls.utils.get_resolution(VIDFN) == (426, 240)
    assert pls.utils.get_framerate(VIDFN) == approx(24.0)


def test_config_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        pls.Livestream(tmp_path / 'nothere.ini', 'localhost')


def test_config_default(tmp_path):
    S = pls.Livestream(None, 'localhost')
    assert 'localhost' in S.site


if __name__ == '__main__':
    pytest.main(['-x', __file__])
