"""Unit tests for SoundcloudMediaProvider (network mocked)."""
from unittest.mock import MagicMock, patch

from mediavocab import Entity, EntityKind, MediaType, Release, Signals, Work
from mediavocab.taxonomy import PlaybackType

from ovos_media_provider_soundcloud import SoundcloudMediaProvider


def _make_release(title):
    return Release(work=Work(title=title, media_type=MediaType.MUSIC),
                   uri=f"https://soundcloud.com/acme/{title}",
                   platform="soundcloud")


def test_instantiation():
    prov = SoundcloudMediaProvider()
    assert prov.name == "soundcloud"
    assert prov.media == {MediaType.MUSIC, MediaType.PLAYLIST}
    assert prov.playback_type == {PlaybackType.AUDIO}
    assert prov.is_available() is True


def test_matches_music_true():
    prov = SoundcloudMediaProvider()
    assert prov.matches(Signals(medium=MediaType.MUSIC)) is True


def test_matches_movie_false():
    prov = SoundcloudMediaProvider()
    assert prov.matches(Signals(medium=MediaType.MOVIE)) is False


def test_search_returns_releases():
    prov = SoundcloudMediaProvider()
    fake = [
        _make_release("foo"),
        _make_release("bar"),
        Entity(name="some artist", kind=EntityKind.PERSON),  # must be dropped
    ]
    fake_sc = MagicMock()
    fake_sc.search.return_value = iter(fake)
    with patch("nuvem_de_som.SoundCloud", return_value=fake_sc) as ctor:
        results = prov.search(Signals(medium=MediaType.MUSIC,
                                      title="foo", artist="acme"))
    ctor.assert_called_once()
    fake_sc.search.assert_called_once()
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(r, Release) for r in results)
    assert [r.work.title for r in results] == ["foo", "bar"]


def test_search_empty_query():
    prov = SoundcloudMediaProvider()
    with patch("nuvem_de_som.SoundCloud") as ctor:
        results = prov.search(Signals(medium=MediaType.MUSIC))
    ctor.assert_not_called()
    assert results == []


def test_search_swallows_backend_errors():
    prov = SoundcloudMediaProvider()
    fake_sc = MagicMock()
    fake_sc.search.side_effect = RuntimeError("boom")
    with patch("nuvem_de_som.SoundCloud", return_value=fake_sc):
        results = prov.search(Signals(title="anything"))
    assert results == []
