#!/usr/bin/env python3
# OBERON (Exalogic) — generátor aktivačného kódu z objednávkového kódu.
# Reprodukovane z Exa.OBERON.ApplicationEnvironment.dll (de4dotEx + ilspycmd,
# triedy Class7/Class8/Class10). Overene na 2 realnych objednavkovych kodoch
# (self-check 4/4 viazanych controlnych znakov).
#
# Pouzitie:  python3 oberon_license.py <ORDER-CODE> [<ORDER-CODE> ...]
# Vystup:    dekodovane polia licencie + AKTIVACNY KOD (29 znakov, 5 blokov).
import re
import sys

ALPHA36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def b36(s):
    v = 0
    for ch in s.upper():
        v = v * 36 + ALPHA36.index(ch)
    return v


def b36enc(v, width=5):
    out = ""
    while v >= 1:
        out = ALPHA36[v % 36] + out
        v //= 36
    return out.rjust(width, "0")


def crc16_bytes(data):
    tab = []
    for i in range(256):
        c = i << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if (c & 0x8000) else (c << 1) & 0xFFFF
        tab.append(c)
    crc = 0
    for b in data:
        crc = ((crc << 8) & 0xFFFF) ^ tab[((crc >> 8) ^ b) & 0xFF]
    return crc


class NetRandom:  # .NET Framework 4.x System.Random(int), exact per corefx compat
    MBIG = 2147483647
    MSEED = 161803398

    def __init__(self, seed):
        MBIG, MSEED = self.MBIG, self.MSEED
        sub = MBIG if seed == -2147483648 else abs(seed)
        a = [0] * 56
        mj = MSEED - sub
        a[55] = mj
        mk, ii = 1, 0
        for _i in range(1, 55):
            ii += 21
            if ii >= 55:
                ii -= 55
            a[ii] = mk
            mk = mj - mk
            if mk < 0:
                mk += MBIG
            mj = a[ii]
        for _k in range(4):
            for i in range(1, 56):
                n = i + 30
                if n >= 55:
                    n -= 55
                a[i] -= a[1 + n]
                if a[i] < 0:
                    a[i] += MBIG
        self.a, self.inext, self.inextp = a, 0, 21

    def _internal(self):
        self.inext += 1
        if self.inext >= 56:
            self.inext = 1
        self.inextp += 1
        if self.inextp >= 56:
            self.inextp = 1
        r = self.a[self.inext] - self.a[self.inextp]
        if r == self.MBIG:
            r -= 1
        if r < 0:
            r += self.MBIG
        self.a[self.inext] = r
        return r

    def sample(self):
        return self._internal() * (1.0 / self.MBIG)

    def next(self, lo, hi):  # Random.Next(min,max) -> [min,max)
        return int(self.sample() * (hi - lo)) + lo


# Abecedy overovacek (presne z dekompilacie): Class8.method_2 (order) a
# Class10.method_1 (activation). Kluc = index pozicie vo 20-slotom zozname.
ORDER_CODE_ALPHABETS = {
    12: "LQASTERFGHYUJKI0LZXSDFVBGHJMK951753",
    13: "IQWETYU0PADFGJKLXCVNM1469",
    18: "XLIAMISC00LISNTHE333",
    19: "CXSAISC00LS0ISC0CAINEANDP0TANDMETH",
}
ACT_CODE_ALPHABETS = {
    12: "7024A8ACEGIKM0QSUWYYY",
    15: "4012678GBCGHIMN0STUYZ",
    19: "3W9764T31QETU0ASFHKZCBM",
}


def build_pattern(code, alphabets_by_idx):
    """Postavi ocakavany regex 29-znakoveho kodu. Vracia (zhoda, pattern, slova)."""
    code = code.strip().upper().replace(" ", "")
    if len(code) != 29:
        return False, None, None
    w1, w2, w3 = b36(code[0:5]), b36(code[6:11]), b36(code[12:17])
    rnd = NetRandom(w1 + w2 + w3)
    pat = code[:17]
    for length in range(17, 29):
        if length % 6 == 5:
            pat += "-"
            continue
        idx = length - (5 + (length + 1) // 6)
        ab = alphabets_by_idx.get(idx)
        if ab:
            pat += ab[rnd.next(0, len(ab) - 1)]
        else:
            pat += "."
            rnd.next(0, 1)
    return re.fullmatch(pat, code) is not None, pat, (w1, w2, w3)


def decode_fields(w1, w2, w3):
    TYPES = {0: "Zadarmo/Zadarmo trial", 1: "Standard", 2: "Multi (viazane na USB kluc)"}
    VALUES = ["Zadarmo/Zadarmo", "Mini", "Standard", "Profi"]
    USERS = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6-10", 7: "11-15",
             8: "16-20", 9: "21-25", 10: "26-30", 11: "31-35", 12: "36-40",
             13: "41 a viac"}
    return {
        "rok": 2000 + (w2 & 0x3F),
        "typ": TYPES.get((w2 >> 6) & 3, "?"),
        "uzivatelia": USERS.get((w2 >> 8) & 0xF, "?"),
        "ucetnictvo": VALUES[w3 & 3],
        "sklad": VALUES[(w3 >> 2) & 3],
        "mzdy": VALUES[(w3 >> 4) & 3],
        "dokumenty/CRM": VALUES[(w3 >> 6) & 3],
        "hotel": VALUES[(w3 >> 8) & 3],
        "crc_firma": (w1 >> 3) & 0x7FFF,
        "crc_ico": (w3 >> 14) & 0x7F,
    }


def make_activation(order_code):
    """Vrstva nad algoritmom: zrkadlovy layout (W1 left, W2<->W3) + ACT abecedy."""
    oc = order_code.strip().upper().replace(" ", "")
    ok, pat, words = build_pattern(oc, ORDER_CODE_ALPHABETS)
    if words is None:
        return None, None, None, False
    w1, w2, w3 = words
    a1, a2, a3 = w1, w3, w2
    out = f"{b36enc(a1)}-{b36enc(a2)}-{b36enc(a3)}"
    rnd = NetRandom(a1 + a2 + a3)
    for length in range(17, 29):
        if length % 6 == 5:
            out += "-"
            continue
        idx = length - (5 + (length + 1) // 6)
        ab = ACT_CODE_ALPHABETS.get(idx)
        if ab:
            out += ab[rnd.next(0, len(ab) - 1)]
        else:
            out += "0"  # wildcard '.' -> libovolny znak; deterministicky '0'
            rnd.next(0, 1)
    return oc, pat, out, ok


# Brana pouzivatelov: Discord user ID -> smi generovat.
ALLOWED_DISCORD_IDS = {"450698194968641561"}
BOT_ENV = "/home/rugent/.hermes/profiles/rudo-vasky/.env"


def _bot_token():
    try:
        with open(BOT_ENV) as fh:
            for ln in fh:
                if ln.startswith("DISCORD_BOT_TOKEN="):
                    return ln.split("=", 1)[1].strip()
    except OSError:
        pass
    return None


def _discord_get(path, token):
    import json as _json
    import urllib.request
    req = urllib.request.Request(
        "https://discord.com/api/v10" + path,
        headers={"Authorization": "Bot " + token,
                 "User-Agent": "hermes-oberon-skill/1.0 (https://exalogic.sk, 1.0)"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return _json.loads(r.read())


def verify_discord(message_id, channel_id):
    """Overi cez Discord API: autor spravy je povoleny a ide o DM (channel type 1).
    Vracia (ok, dovod_zamitnutia)."""
    token = _bot_token()
    if not token:
        return False, "nemozem nacitat DISCORD_BOT_TOKEN"
    if not (message_id and channel_id):
        return False, "chyba --message a/alebo --channel"
    try:
        ch = _discord_get(f"/channels/{channel_id}", token)
        if ch.get("type") != 1:
            return False, "sprava nie je v sukromnom (DM) kanale"
        msg = _discord_get(f"/channels/{channel_id}/messages/{message_id}", token)
    except Exception as exc:
        return False, f"Discord API: {exc}"
    author = (msg.get("author") or {}).get("id")
    if author not in ALLOWED_DISCORD_IDS:
        return False, f"autor spravy je ID {author}"
    return True, None


def main(argv):
    user = message = channel = None
    codes = []
    it = iter(argv)
    for a in it:
        if a == "--user":
            user = next(it, None)
        elif a == "--message":
            message = next(it, None)
        elif a == "--channel":
            channel = next(it, None)
        else:
            codes.append(a)
    if not codes:
        print("Pouzitie: python3 oberon_license.py --message <MSG_ID> --channel <CHANNEL_ID> <ORDER-CODE> [...]")
        return 2
    if message or channel:  # tvrdsie overenie: primamo cez Discord API
        ok, why = verify_discord(message, channel)
        if not ok:
            print(f"ZAMITNUTE: {why}.")
            return 77
    elif user not in ALLOWED_DISCORD_IDS:  # manual rezim (bez Discord API)
        print("ZAMITNUTE: tento skill smie pouzit len autorizovany pouzivatel "
              f"(ID {sorted(ALLOWED_DISCORD_IDS)}). Pozadovatel: {user or 'neuvedene ID'}.")
        return 77
    rc = 0
    for arg in codes:
        oc, pat, act, selfcheck = make_activation(arg)
        print(f"Objednávkový kód : {arg.upper().replace(' ', '')}")
        if act is None:
            print("CHYBA: kód nemá 29 znakov alebo obsahuje neplatné znaky (iba 0-9A-Z a pomlčky).")
            rc = 1
            continue
        _, _, (w1, w2, w3) = build_pattern(oc, ORDER_CODE_ALPHABETS)
        f = decode_fields(w1, w2, w3)
        print(f"Licencia         : {f['rok']}, {f['typ']}, užívatelia {f['uzivatelia']}, "
              f"Účto={f['ucetnictvo']}, Sklad={f['sklad']}, Mzdy={f['mzdy']}, "
              f"Doc={f['dokumenty/CRM']}, Hotel={f['hotel']}")
        if not selfcheck:
            print("UPOZORNENIE: self-check controlných znakov nesedí — kód môže byť")
            print("poškodený, z iného roku/verzie, alebo z iného produktu. Kód nižšie")
            print("je predom vygenerovaný, ale pred použitím ho over.")
            rc = 1
        print(f"AKTIVACNY KOD    : {act}")
        print()
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
