# ovos-media-provider-soundcloud

An OVOS **MediaProvider** plugin for SoundCloud. It replaces the deprecated OCP search skill [`ovos-skill-soundcloud`](https://github.com/OpenVoiceOS/ovos-skill-soundcloud).

The OCP pipeline used to broadcast `ovos.common_play.query` over the bus and wait for skills to answer. Now it loads MediaProvider plugins in-process, gates them by routing, and calls `search()` directly. This plugin wraps the [`nuvem_de_som`](https://github.com/OpenJarbas/nuvem_de_som) SoundCloud client. Its orchestrator, `SoundCloud.search()`, already returns [`mediavocab.Release`](https://github.com/TigreGotico/mediavocab) objects. The plugin drops artist and user identity hits (`mediavocab.Entity`), because a MediaProvider returns playable media, not identities.

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

OCP finds the plugin through this entry point:

```toml
[project.entry-points."opm.media.provider"]
soundcloud = "ovos_media_provider_soundcloud:SoundcloudMediaProvider"
```

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `max_results` | `10` | Maximum number of results returned per search. |

## Related projects

- [`ovos-skill-soundcloud`](https://github.com/OpenVoiceOS/ovos-skill-soundcloud): the deprecated OCP skill this plugin replaces.
- [`nuvem_de_som`](https://github.com/OpenJarbas/nuvem_de_som): the SoundCloud client this plugin wraps.
- [`mediavocab`](https://github.com/TigreGotico/mediavocab): defines the `Release` and `Entity` objects the client returns.

## License

Apache-2.0
</content>
