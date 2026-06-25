"""SoundCloud MediaProvider plugin for OVOS.

Wraps the :mod:`nuvem_de_som` SoundCloud client and exposes SoundCloud search to
the OCP pipeline as a
:class:`~ovos_plugin_manager.templates.media_provider.MediaProvider`. Replaces
the deprecated OCP search skill ``ovos-skill-soundcloud``.

``nuvem_de_som`` already emits :class:`mediavocab.Release` objects directly from
its orchestrator's combined ``SoundCloud.search`` (tracks + set tracks + artist
tracks), so this provider is a thin routing/filtering shim over the public
search API: artist/user hits (:class:`mediavocab.Entity`) are dropped because a
MediaProvider returns playables, not identities.
"""
from typing import ClassVar, List, Optional, Set

from ovos_utils.log import LOG

from mediavocab import Entity, Release, Signals

from ovos_plugin_manager.templates.media_provider import MediaProvider

from ovos_media_provider_soundcloud.version import __version__  # noqa: F401


class SoundcloudMediaProvider(MediaProvider):
    """Search SoundCloud's public catalog and return playable music releases."""

    name: ClassVar[str] = "soundcloud"

    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        # max results per search, overridable via plugin config
        self.max_results: int = int(self.config.get("max_results", 10))

    def search(self, signals: Signals, lang: str = "en-us", *,
               supported_playback_types: Optional[Set[str]] = None,
               blocked_genres: Optional[Set[str]] = None,
               region: Optional[str] = None,
               session_id: Optional[str] = None) -> List[Release]:
        """Search SoundCloud for ``signals.title`` (optionally scoped by
        ``signals.artist``) and return candidate :class:`Release` objects.

        Tracks and sets are returned as ``Release`` by ``nuvem_de_som``;
        artist/user identity hits (:class:`mediavocab.Entity`) are dropped — a
        MediaProvider returns playables, not identities.
        """
        title = (signals.title or "").strip()
        artist = (signals.artist or "").strip()
        query = " ".join(p for p in (artist, title) if p).strip()
        if not query:
            return []

        from nuvem_de_som import SoundCloud

        results: List[Release] = []
        try:
            sc = SoundCloud()
            for item in sc.search(query, limit=self.max_results):
                if isinstance(item, Release):
                    results.append(item)
                elif isinstance(item, Entity):
                    # artist/user identity hits are not playable
                    continue
        except Exception:
            LOG.exception(f"SoundCloud search failed for query: {query!r}")
            return []
        return results
