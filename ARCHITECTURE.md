# Architecture

## Purpose and boundaries

Publishes a static AltStore-format source (`source.json`) that points at the
fcitx5-ios nightly IPA. It stores metadata only; the IPA stays on the upstream
GitHub release.

```
 fcitx-contrib/fcitx5-ios            this repository                    iPhone
 ┌──────────────────────┐   API   ┌───────────────────────────┐  raw   ┌──────────────────┐
 │ release tag `latest` │ ──────► │ update.yml (every 6 h)    │ ─────► │ SideStore /      │
 │  └ Fcitx5.ipa        │         │  └ update_source.py       │  URL   │ AltStore/Feather │
 └──────────┬───────────┘         │      └ writes source.json │        └────────┬─────────┘
            │                     └───────────────────────────┘                 │
            └──────────────── IPA downloaded directly from upstream ◄───────────┘
```

## Modules

- `scripts/update_source.py`: standard-library Python. Fetches
  `repos/fcitx-contrib/fcitx5-ios/releases/tags/latest`, picks the `Fcitx5.ipa`
  asset and writes `source.json`. Exits non-zero if the asset is missing, so
  the workflow never publishes a broken source. Writes nothing when the output
  is unchanged.
- `.github/workflows/update.yml`: runs the script on a schedule and on manual
  dispatch, and commits `source.json` only when it changed. Uses the built-in
  `GITHUB_TOKEN` (contents: write).
- `source.json`: the published artifact, served through
  `raw.githubusercontent.com`.

## Data model

One source, one app (`org.fcitx.Fcitx5`), one version entry describing the
current nightly. Version is `0.1.0.<YYYYMMDDHHMM>` from the asset's
`updated_at` (UTC), because upstream never bumps its own version. The download
URL is the fixed `releases/download/latest/Fcitx5.ipa`.

## Constraints

- No binaries or credentials live in this repository.
- The version shown in the source differs from the app's own
  `CFBundleShortVersionString` (`0.1.0`); some clients may therefore keep
  offering the build as an update after installation.
