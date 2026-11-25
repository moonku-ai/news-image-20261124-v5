# THE WORLD IN ONE DAY — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261124)

One image that sums up the world's news of **Tuesday 24 November 2026**:
38 stories, every one dated that day — 3 illustrated heroes, 12 illustrated
medium stories, 23 more in "Also on Tuesday", a six-number stats strip, an
hour-by-hour timeline, a world map with 37 numbered pins, and a DATE CHECK
listing the other days' news that was deliberately left out.

Entry for the [make.fun bounty "Sum up 24 November's world news in one
image"](https://make.fun/bounty/news-image-20261124) ($100, top 50 share).

## How it runs

Pure Python standard library, no network, no third-party packages:

```sh
python3 main.py            # writes entry-v5.png and entry.png here
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png (grader path)
python3 test_main.py       # atlas, wrap, render, determinism, clean-dir
```

`main.py` draws the broadsheet (1024x1024 PNG) from `atlas.bin`, a glyph
atlas built at build time by `tools/make_atlas.py` (PIL, build-time only).
The program never crashes: every output write is guarded, and if drawing
ever failed it would fall back to the pre-rendered `entry-v5.png` shipped
in the repo. Runs in ~0.5 s, byte-identical on every run.

## Stories (all dated Tuesday 24 November 2026)

- **Heroes:** Asia chip stocks surge (Kospi +6.32%) · three tankers hit by
  mines in Hormuz, Guards say · Russian drones hit Zaporizhzhia overnight.
- **Medium:** Russian drone enters Polish airspace · Seoul warns Ulleung
  island · Sanofi buys Insmed for $41bn · CAS restores Senegal as AFCON
  champions · Nepal quake M5.6 · Cikande factory-fire toll 26 · Israeli
  strikes kill seven in Gaza · Hasina to fly home 16 Dec · Solomons ends
  China security pact · Bougainville votes on nationhood · Trump meets
  NATO chief Rutte · SoftBank puts $2bn into Intel.
- **Also on Tuesday (23 more):** Iraq oilfields, EU hybrid cap, El Chapo
  Isidro, Hanoi blast, Australia big-tech fines, Galapagos floods, Tigray,
  Modi AI centre, Bangladesh typhoid drive, Megaspeed blacklist,
  BepiColombo, Tajikistan leaves ICC, Villavicencio car bomb, Rohingya
  return, UN femicide report, South Africa water curbs, England level T20,
  Huawei convicted, Houthi Riyadh strike, UK heat deaths, Guterres AI
  rules, Indonesia VP candidates, Trump warns Iran.

Sources per story: Reuters, AP, AFP, Yonhap, Antara, UN, CAS, NATO, EU.
