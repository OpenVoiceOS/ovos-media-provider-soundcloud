"""Unit tests for SoundcloudMediaProvider (network mocked)."""
from unittest.mock import MagicMock, patch

from mediavocab import Entity, EntityKind, MediaType, Release, Signals, Work

from ovos_media_provider_soundcloud import SoundcloudMediaProvider


def _make_release(title):
    return Release(work=Work(title=title, media_type=MediaType.MUSIC),
                   uri=f"https://soundcloud.com/acme/{title}",
                   platform="soundcloud")


def test_instantiation():
    prov = SoundcloudMediaProvider()
    assert prov.name == "soundcloud"


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


def test_search_accepts_context_kwargs():
    """The provider accepts the pipeline's request-context kwargs."""
    prov = SoundcloudMediaProvider()
    fake_sc = MagicMock()
    fake_sc.search.return_value = iter([_make_release("foo")])
    with patch("nuvem_de_som.SoundCloud", return_value=fake_sc):
        results = prov.search(
            Signals(medium=MediaType.MUSIC, title="foo"),
            lang="en-us",
            supported_playback_types={"audio"},
            blocked_genres={"adult"},
            region="US",
            session_id="sess-1",
        )
    assert len(results) == 1
    assert all(isinstance(r, Release) for r in results)


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
