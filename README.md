# fcitx5-ios source

Unofficial AltStore / SideStore / Feather source for the
[fcitx5-ios](https://github.com/fcitx-contrib/fcitx5-ios) nightly build.

Add this URL to the Sources page of your sideloading app:

```
https://raw.githubusercontent.com/PapainTea/fcitx5-ios-source/main/source.json
```

A GitHub Actions workflow checks the upstream `latest` release every six hours
and refreshes `source.json` when a new IPA is published. The IPA itself is
downloaded straight from the upstream release; this repository hosts no binaries.

Upstream keeps the app version at `0.1.0`, so the source uses
`0.1.0.<UTC publish time>` (for example `0.1.0.202610092309`) to tell nightly
builds apart.

Run `python3 scripts/update_source.py` to regenerate the file locally.
