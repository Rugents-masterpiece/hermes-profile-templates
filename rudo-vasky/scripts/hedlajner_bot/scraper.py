#!/usr/bin/env python3
"""Ranny sumar z Hedlajnera (hedlajner.sk) pre Discord kanál prúdnica.

Volá sa z Hermes cron joba (no_agent), jeho stdout sa posiela na Discord.
Webhook sa v tejto verzii nepouziva — dorucenie riesi Hermes delivery.
"""
import sys
import requests
from bs4 import BeautifulSoup

URL = "https://hedlajner.sk/"


def get_hedlajner_summary():
    try:
        response = requests.get(
            URL, timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"},
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Nepodarilo sa stiahnuť {URL}: {type(e).__name__}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Hlavna stranka pouziva <article> alebo <h2>/<h3> ako headline.
    # Vyberame prve realne clanky (min. 20 znakov), bez globalnych textov.
    seen = set()
    titles = []

    def add(title):
        nonlocal titles
        if not title or title in seen:
            return
        # filce: mriezka a paticka
        if "Hlavné správy" in title or "hedlajner.sk" in title.lower():
            return
        if title in ("Domov", "Správy", "O nás", "Kontakt"):
            return
        if len(title) < 20:
            return
        seen.add(title)
        titles.append(title)

    # 1) Primárny zdroj: <article> ... headline (typicky format)
    for art in soup.find_all("article"):
        h = art.find(["h1", "h2", "h3", "h4"])
        if h:
            add(" ".join(h.get_text().split()))
        if len(titles) >= 5:
            break

    # 2) Sekundárny zdroj: vsetky h2/h3 v hlavnom obsahu
    if len(titles) < 5:
        for h in soup.find_all(["h2", "h3"]):
            add(" ".join(h.get_text().split()))
            if len(titles) >= 5:
                break

    if not titles:
        return None

    lines = ["Ranný sumár z Hedlajnera:", ""]
    for t in titles:
        lines.append(f"• {t}")
    return "\n".join(lines)


if __name__ == "__main__":
    out = get_hedlajner_summary()
    if out:
        print(out)
