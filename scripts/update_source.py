#!/usr/bin/env python3
"""Generate an AltStore/SideStore/Feather source for the fcitx5-ios nightly build.

Reads the `latest` release of fcitx-contrib/fcitx5-ios through the GitHub API
and writes source.json. The download URL never changes, so only the version,
date and size are refreshed. The upstream app version is fixed at 0.1.0, so the
nightly publish time is appended to make every build look like a new version.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UPSTREAM = "fcitx-contrib/fcitx5-ios"
TAG = "latest"
ASSET = "Fcitx5.ipa"
BASE_VERSION = "0.1.0"
OUTPUT = Path(__file__).resolve().parent.parent / "source.json"


def fetch_release():
    req = urllib.request.Request(
        f"https://api.github.com/repos/{UPSTREAM}/releases/tags/{TAG}",
        headers={"Accept": "application/vnd.github+json"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def build_source(release):
    asset = next((a for a in release["assets"] if a["name"] == ASSET), None)
    if asset is None:
        sys.exit(f"{ASSET} not found in release {TAG}")

    built = datetime.strptime(asset["updated_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    version = f"{BASE_VERSION}.{built:%Y%m%d%H%M}"

    return {
        "name": "Fcitx5 iOS Nightly",
        "identifier": "io.github.papaintea.fcitx5-ios-source",
        "subtitle": "Unofficial source for the fcitx5-ios nightly build",
        "website": f"https://github.com/{UPSTREAM}",
        "apps": [
            {
                "name": "Fcitx5",
                "bundleIdentifier": "org.fcitx.Fcitx5",
                "developerName": "fcitx-contrib",
                "subtitle": "Fcitx5 input method framework for iOS",
                "localizedDescription": (
                    "Fcitx5 input method framework ported to iOS 16.3 or later. "
                    "Developer beta, built nightly from the master branch."
                ),
                "iconURL": "https://raw.githubusercontent.com/fcitx/fcitx5/master/data/icon/128x128/apps/org.fcitx.Fcitx5.png",
                "tintColor": "3584E4",
                "category": "utilities",
                "versions": [
                    {
                        "version": version,
                        "date": built.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "localizedDescription": f"Nightly build published {built:%Y-%m-%d %H:%M} UTC.",
                        "downloadURL": asset["browser_download_url"],
                        "size": asset["size"],
                        "minOSVersion": "16.3",
                    }
                ],
                "appPermissions": {"entitlements": [], "privacy": {}},
            }
        ],
        "news": [],
    }


def main():
    source = build_source(fetch_release())
    text = json.dumps(source, indent=2, ensure_ascii=False) + "\n"
    if OUTPUT.exists() and OUTPUT.read_text() == text:
        print("source.json is up to date")
        return
    OUTPUT.write_text(text)
    print(f"source.json updated: {source['apps'][0]['versions'][0]['version']}")


if __name__ == "__main__":
    main()
