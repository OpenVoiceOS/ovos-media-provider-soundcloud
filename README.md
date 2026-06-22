# ovos-media-provider-soundcloud

OVOS **MediaProvider** plugin for SoundCloud. Replaces the deprecated OCP search
skill [`ovos-skill-soundcloud`](https://github.com/OpenVoiceOS/ovos-skill-soundcloud).

Instead of broadcasting `ovos.common_play.query` over the bus and waiting for
skills to answer, the OCP pipeline loads MediaProvider plugins in-process, gates
them by routing, and calls `search()` directly. This plugin wraps the
[`nuvem_de_som`](https://github.com/OpenJarbas/nuvem_de_som) SoundCloud client,
whose orchestrator `SoundCloud.search()` already yields
[`mediavocab.Release`](https://github.com/TigreGotico/mediavocab) objects.
Artist/user identity hits (`mediavocab.Entity`) are dropped — a MediaProvider
returns playables, not identities.

## Install

```bash
pip install ovos-media-provider-soundcloud
```

## Routing

| Axis | Value |
|------|-------|
| `media` | `MUSIC`, `PLAYLIST` |
| `playback_type` | `AUDIO` |
| `genre_filter` | *(none)* |

## Entry point

```toml
[project.entry-points."opm.media.provider"]
soundcloud = "ovos_media_provider_soundcloud:SoundcloudMediaProvider"
```

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `max_results` | `10` | Maximum number of results returned per search. |

## License

Apache-2.0
