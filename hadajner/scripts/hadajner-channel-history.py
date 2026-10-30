#!/usr/bin/env python3
"""Vytlacis dzisna spravy z Discord kanala pre cron job profilu hadajner."""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

CHANNEL = "1563619172183703605"
PROFILE_ENV = "/home/rugent/.hermes/profiles/hadajner/.env"


def token():
    tok = os.environ.get("DISCORD_BOT_TOKEN")
    if tok:
        return tok.strip()
    try:
        with open(PROFILE_ENV, encoding="utf-8") as f:
            for ln in f:
                if ln.startswith("DISCORD_BOT_TOKEN="):
                    return ln.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return None


def main():
    tok = token()
    if not tok:
        print("HISTORIA: nedari sa citat (chba bot token)")
        return
    url = (f"https://discord.com/api/v10/channels/{CHANNEL}/messages?limit=50")
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bot {tok}",
                      "User-Agent": "Hermes-Hadajner (self, 1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            msgs = json.load(r)
    except Exception as e:  # noqa: BLE001
        print(f"HISTORIA: nedari sa citat ({type(e).__name__})")
        return
    today = datetime.now(ZoneInfo("Europe/Bratislava")).date()
    lines = []
    for m in reversed(msgs):
        try:
            ts = datetime.fromisoformat(m["timestamp"]).astimezone(
                ZoneInfo("Europe/Bratislava"))
        except (KeyError, ValueError):
            continue
        if ts.date() != today:
            continue
        author = (m.get("author") or {}).get("username", "?")
        text = re.sub(r"\s+", " ", m.get("content") or "").strip()[:180]
        if not text and m.get("attachments"):
            text = "[priloha]"
        if text:
            lines.append(f"[{ts:%H:%M}] {author}: {text}")
    if not lines:
        print("HISTORIA: dnes zatial ziadne spravy v kanali")
        return
    out = ["HISTORIA kanala za dnes (najnovsie dole):"] + lines[-30:]
    print("\n".join(out)[:4000])


if __name__ == "__main__":
    sys.exit(main())
