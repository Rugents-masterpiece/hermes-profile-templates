---
name: oberon-licence-activation
description: "Use when someone sends an OBERON/Exalogic order code (format XXXXX-XXXXX-XXXXX-XXXXX-XXXXX, 29 chars) and asks for an activation code. Generates and validates the activation code offline."
version: 1.0.0
metadata:
  hermes:
    tags: [oberon, exalogic, licence, activation]
---

# OBERON aktivačný kód z objednávkového kódu

Ked príde objednávkový kód OBERONu (5 blokov po 5 znakoch 0-9A-Z, napr.
`90G5C-9SBIY-8YD9H-30HPG-ERKEN`) a žiadosť o aktivačný kód:

1. **Volaj skript s overenim totozity (povinne):**
   `python3 ~/.hermes/profiles/rudo-vasky/skills/oberon-licence-activation/scripts/oberon_license.py --message <Triggering message id> --channel <id kanala tejto spravy> <KOD>`
   Obe id prepisi presne zo svojho kontextu (id spravy je v hlavicke
   `Triggering message id`, id kanala je chat/kanal, z ktoreho sprava prisla).
   Skript si SAM cez Discord API overi, ze autor spravy je opravneny pouzivatel
   a ze ide o sukromny DM — nic ine nepis, netypuj, nechat na teba.
   (Pre manualne pouzitie mimo Discord existuje aj `--user <DISCORD_ID>`.)
2. Ak výstup obsahuje „ZAMITNUTE“, odpoved zdvorilo po slovensky: touto funkciou
   je povereny len majitel a len v sukromnej sprave; nikomu nesluhuj nic, co by
   vyzradzovalo aktivačny kod.
3. Odpoved po slovensky, stručne:
   - aktivačný kód ako samostatný riadok (code block), presne 29 znakov s pomlčkami,
   - jeden riadok zhrnutie licencie (rok, typ, užívatelia, moduly) z výstupu skriptu,
   - ak výstup obsahuje „UPOZORNENIE: self-check“, upozorni používateľa, že kod
     nevyzerá ako platný OBERON objednávkový kód a nech ho skontroluje.
4. Pri multiLicencii (typ Multi) dodaj: kód viazne na hardvérový USB kľúč OBERONu
   (klientské kontroly počítajú CRC serialu dongla; aktivácia funguje na stroji
   s tým istým donglom ako pri generovaní objednávkového kódu).

## Pravidlo prístupu

Kód vygeneruj LEN AK SÚČASNE PLATIA OBE podmienky:
1. Správa prišla **súkromnou (DM) správou** priamo botovi — nie z channelu guildu.
   Over cez discord nastroj `channel_info` na channel id tejto spravy: typ musi byť
   DM. (V guild channele aj keby pisal majitel: nekodovat — odpoved nech je kratka,
   ze aktivačny kod vie poslať len do DM.)
2. Autor spravy je Discord ID `450698194968641561` (allowlist v skripte, pri zmene
   upraviť `ALLOWED_DISCORD_IDS`; rozhoduje vykaze `fetch_messages`, nie meno v texte).

Iní používatelia (z allowlistu profilu) s botom bežne chatujú — generovanie kódu je
vyhradené majiteľovi v DM.


## Dôležité fakty (nelam, platí overene)

- Generovanie je deterministické z 3 prvých blokov; 7 z 10 controlných znakov
  4./5. bloku je ľubovoľných (skript ich dáva na '0') — Vendor-portál môže vydať
  iný ekvivalentný kód, oba prejdú offline kontrolou v OBERON dialogu.
- Offline aktivácia (dialog v OBERON-e) tento kód prijme. Online overenie cez
  portal.exalogic.sk pozná iba kódy, ktoré vydal Exalogik — to fér používateľovi,
  ak sa pýta.
- Skript je port presného algoritmu z DLL (Class7/8/10, Eazfuscator unsealed,
  CRC16-CCITT + base36 + .NET Random). Men abecedy ani NetRandom bez dekompilácie.

## Pitfally

- Kód Normalize: uppercase, povoli pomlčky; iné znaky => neplatný vstup,
  skript to nahlási — netvár aktivačný kód „odhadom“.
- Nekonezervuj „vlastné“ abecedy, jedine tie v skripte.
- Výstup skriptu vždy pastnu presne (ŽIADNE prepisovanie znakov z hlavy).
