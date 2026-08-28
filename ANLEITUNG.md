# Wolfpack Feuerleitrechner — Veröffentlichen auf Steam

## Was in diesem Ordner liegt

| Datei | Zweck |
|---|---|
| `index.html` | Der Rechner. Zweisprachig (DE/EN), komplett eigenständig, keine externen Dateien. |
| `STEAM-GUIDE-DE.txt` | Fertiger deutscher Steam-Guide zum Reinkopieren (BBCode). |
| `STEAM-GUIDE-EN.txt` | Dasselbe auf Englisch. |
| `guide-aob-*.png` | Titelbild für den Guide (Station 04, Bugwinkel) — je Sprache eines. |
| `guide-rec-*.png` | Zweites Bild (Station 01, Schiffserkennung) — je Sprache eines. |
| `ANLEITUNG.md` | Diese Datei. |

Die Originaldatei `..\wolfpack-feuerleitrechner.html` bleibt unverändert liegen.

---

## Warum kein Workshop-Item?

Der **Steam Workshop** ist ein Ablagesystem für Spielinhalte — Missionen, Modelle, Skins. Ein Spiel muss den Workshop aktiv unterstützen, und der Inhalt muss etwas sein, das *im Spiel* geladen wird. Wolfpack bindet keinen Workshop ein, und eine Webseite wäre auch bei einem Spiel, das ihn hat, kein ladbarer Inhalt.

Der passende Weg auf Steam ist ein **Community-Guide**. Der taucht direkt auf der Wolfpack-Shopseite unter „Guides" auf, ist durchsuchbar, kann bewertet und kommentiert werden — und lässt sich im Spiel über das Steam-Overlay aufrufen. Praktisch genau das, was ein Workshop-Item hier leisten würde.

---

## Schritt 1 — Den Rechner ins Netz stellen — **erledigt**

Das Steam-Overlay hat einen eingebauten Browser, aber der kann **keine lokalen Dateien** öffnen
(`file:///C:/...` funktioniert dort nicht). Deshalb liegt der Rechner jetzt hier:

**<https://rannau02-code.github.io/wolfpack-fire-control/>**

Repository: <https://github.com/rannau02-code/wolfpack-fire-control> (public — bei einem
privaten Repository schaltet GitHub Pages die Seite nicht frei).

Der Ordner auf dem Desktop ist gleichzeitig das Arbeitsverzeichnis dieses Repositories.

---

## Schritt 2 — Den Guide veröffentlichen

Für jede Sprache **ein eigener Guide**. Steam sortiert Guides nach Sprache und zeigt Spielern bevorzugt ihre eigene — zwei Guides erreichen deutlich mehr Leute als einer mit beiden Sprachen untereinander.

1. Steam öffnen → **Bibliothek** → Rechtsklick auf **Wolfpack** → **Community-Hub anzeigen**.
2. Oben auf **Guides** → rechts auf **Guide erstellen**.
3. Aus `STEAM-GUIDE-DE.txt`:
   - **Titel** und **Beschreibung** aus dem Kopf der Datei übernehmen.
   - Alles ab der Zeile `--- AB HIER ... ---` in das große Textfeld kopieren.
   - Der Link steht schon drin, es ist nichts mehr zu ersetzen.
4. **Sprache:** Deutsch. **Typ:** Gameplay Basics.
5. Bilder hochladen — Steam verlangt mindestens eines. Liegen fertig im Ordner:
   - `guide-aob-de.png` als **Titelbild** (die grüne Phosphoranzeige zieht in der Guide-Liste am meisten Blick auf sich)
   - `guide-rec-de.png` weiter unten im Text, beim Abschnitt zur Schiffserkennung

   Für den englischen Guide entsprechend `guide-aob-en.png` und `guide-rec-en.png`.
6. Sichtbarkeit **Öffentlich** → **Speichern und fortfahren**.
7. Das Ganze noch einmal mit `STEAM-GUIDE-EN.txt`, Sprache Englisch.

Am Ende in beiden Guides jeweils einen Kommentar mit dem Link zum anderen setzen — dann finden Leute die passende Fassung.

---

## Schritt 3 — Overlay einrichten

So benutzen die Leser es später, und so sollte man es einmal selbst testen:

1. Wolfpack starten — **randloses Fenster**, nicht exklusives Vollbild. Im echten Vollbild flackert das Overlay auf manchen Grafikkarten oder verliert den Fokus.
2. **Shift + Tab** (Steams Voreinstellung, frei belegbar) → Overlay öffnet sich.
3. Unten links **Webbrowser** → Adresse eingeben → Enter.
4. Stern in der Adresszeile → als Lesezeichen speichern.

Falls Shift+Tab nichts tut: Steam → *Einstellungen* → *Im Spiel* → **Steam-Overlay im Spiel aktivieren** anhaken. Zusätzlich lässt sich das pro Spiel abschalten — Rechtsklick auf Wolfpack → *Eigenschaften* → *Allgemein* nachsehen.

Das Overlay speichert `localStorage`, deshalb bleibt die Sprachwahl auch dort erhalten.

---

## Wenn der Rechner später geändert wird

`index.html` bearbeiten, im Browser prüfen, dann aus diesem Ordner heraus:

```
git add -A
git commit -m "Kurz was geaendert wurde"
git push
```

Nach ein bis zwei Minuten ist die Änderung unter derselben Adresse live. Die Guides auf
Steam müssen dafür nicht angefasst werden.

Neue Texte gehören in beide Sprachblöcke in `index.html` — ganz oben im `<script>`-Teil unter `var I18N = { de: {...}, en: {...} }`. Jeder Schlüssel muss in beiden Blöcken existieren; fehlt einer im englischen, fällt die Seite an dieser Stelle stillschweigend auf Deutsch zurück.

Im HTML steuern vier Attribute die Übersetzung:

- `data-t` — ersetzt den reinen Text des Elements
- `data-th` — ersetzt den Inhalt inklusive Formatierung (`<b>`, `<span>` …)
- `data-tp` — ersetzt den Platzhaltertext eines Eingabefeldes
- `data-ta` — ersetzt die Vorlesehilfe (`aria-label`)
