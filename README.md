# Wolfpack Fire Control Calculator

A fire control calculator for the submarine simulator **Wolfpack** — speed, range and
angle on the bow for the TDC. Bilingual (Deutsch / English), runs entirely offline,
no install, no tracking, nothing but a single HTML file.

**→ [Open the calculator](https://rannau02-code.github.io/wolfpack-fire-control/)**

Built for the Steam Overlay: press `Shift + Tab` in game, open the web browser,
bookmark the page. Works just as well on a second monitor or a phone.

## Stations

| # | Station | What it does |
|---|---|---|
| 01 | Recognition | Mast code (M/K/F) bow to stern, class reference, carries target data into the other stations |
| 02 | Speed | Stopwatch timing bow-to-stern, plus the lateral method for targets not running abeam |
| 03 | Range | Mast height against centiradians, with a cross-check in reverse |
| 04 | AoB | Bearing and target course to angle on the bow, plus the precise length/height ratio method |
| 05 | Course | Bearing and angle on the bow to the target's course |

## Language

The switch sits in the top right. The choice is remembered in `localStorage`; on a first
visit the page follows the browser language. Nothing else is stored, and nothing leaves
the machine.

## Editing

All strings live in the `I18N` object at the top of the `<script>` block, with a `de` and
an `en` section. Every key must exist in both — a key missing from `en` silently falls
back to German. Four attributes drive the markup:

- `data-t` — replaces the element's text
- `data-th` — replaces the content including markup (`<b>`, `<span>` …)
- `data-tp` — replaces an input's placeholder
- `data-ta` — replaces the `aria-label`

Number formatting follows the active language: `1.600 m / 4,2 kn` in German,
`1,600 m / 4.2 kn` in English.

---

Not affiliated with Usurpator AB. Wolfpack is their game; this is a calculator that
happens to be useful next to it.
