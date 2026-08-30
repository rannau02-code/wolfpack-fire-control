# -*- coding: utf-8 -*-
"""U-Boot Typ VII/C, Dreiviertelansicht, Neon gestrichelt.
Erzeugt zwei HTML-Dateien zum headless-Rendern: breit und quadratisch."""
import io, math

# Bootskontur in lokalen Koordinaten. Bug (105,286), Heck (903,186), Steven bis (146,380).
BOOT = '''
  <!-- Decksoberseite: Backbordkante uns zugewandt -->
  <path class="near" stroke-dasharray="14 8"
        d="M105 286 C 150 296, 210 292, 268 282
           C 380 262, 500 240, 620 220
           C 730 202, 830 192, 900 186"/>
  <!-- Steuerbordkante, abgewandt und darueber -->
  <path class="mid" stroke-dasharray="10 8" opacity=".85"
        d="M105 286 C 152 276, 214 266, 286 256
           C 400 240, 512 226, 626 212
           C 736 199, 834 190, 900 186"/>

  <!-- Steven: runder Atlantikbug faellt ins Wasser -->
  <path class="near" stroke-dasharray="12 7"
        d="M105 286 C 84 320, 96 358, 146 380"/>

  <!-- Bordwand Backbord bis zur Wasserlinie -->
  <path class="near" stroke-dasharray="15 9"
        d="M146 380 C 220 372, 300 356, 388 336
           C 500 310, 620 282, 730 250
           C 806 229, 862 212, 888 202"/>
  <!-- Heck geschlossen -->
  <path class="mid" stroke-dasharray="6 5"
        d="M888 202 C 896 198, 900 192, 900 186"/>

  <!-- Spanten geben dem Rumpf Rundung -->
  <g class="deep" stroke-dasharray="5 8">
    <path d="M214 288 C 226 320, 228 348, 218 372"/>
    <path d="M330 268 C 342 296, 344 320, 334 342"/>
    <path d="M452 248 C 462 272, 464 292, 456 310"/>
    <path d="M574 228 C 582 248, 584 264, 578 278"/>
    <path d="M690 208 C 696 224, 698 236, 694 248"/>
  </g>

  <!-- Deckgeschuetz 8,8 cm -->
  <g class="mid" stroke-dasharray="5 4">
    <path d="M470 246 L470 230 L490 228 L490 243"/>
    <path d="M474 229 L 424 214"/>
  </g>

  <!-- Turm: schmale Frontflaeche, breite Backbordflaeche -->
  <path class="near" stroke-dasharray="11 6"
        d="M594 232 L 594 166 L 620 160 L 620 226 Z"/>
  <path class="near" stroke-dasharray="11 6"
        d="M620 160 L 726 146 L 726 208 L 620 226"/>
  <path class="far" stroke-dasharray="4 5" opacity=".65" d="M624 174 L 722 161"/>

  <!-- Wintergarten mit Reling -->
  <path class="mid" stroke-dasharray="6 5"
        d="M726 208 L 782 200 L 782 182 L 726 190"/>
  <g class="far" stroke-dasharray="3 4" opacity=".7">
    <path d="M726 199 L 782 191"/>
    <path d="M740 205 V 188"/><path d="M756 203 V 186"/><path d="M772 201 V 184"/>
  </g>

  <!-- Bruecke: Sehrohre, Peilrahmen, Antennenmast -->
  <g class="mid" stroke-dasharray="5 4">
    <path d="M656 156 V 74"/>
    <path d="M676 153 V 92"/>
  </g>
  <g class="far" stroke-dasharray="3 4">
    <path d="M646 108 h 18"/>
    <path d="M700 150 V 112"/>
  </g>
  <circle cx="676" cy="87" r="4.5" class="far" stroke-dasharray="2.4 2.4"/>

  <!-- Netzabweiser -->
  <path class="wire" stroke-dasharray="2.5 6" opacity=".85"
        d="M105 284 L 596 170 M 782 186 L 898 184"/>

  <!-- Achterdeck in die Ferne -->
  <path class="far" stroke-dasharray="6 6" opacity=".8"
        d="M726 208 C 790 202, 856 194, 900 187"/>

  <!-- Bugwelle -->
  <path class="near" stroke-dasharray="11 8" opacity=".9"
        d="M22 372 C 60 336, 106 320, 152 332"/>
  <g class="mid" stroke-dasharray="9 9" opacity=".65">
    <path d="M0 402 C 56 356, 124 336, 186 350"/>
    <path d="M150 336 C 208 318, 276 320, 330 334"/>
  </g>
  <g class="far" stroke-dasharray="6 10" opacity=".4">
    <path d="M0 418 C 78 368, 168 348, 236 364"/>
    <path d="M322 330 C 396 318, 470 314, 536 322"/>
  </g>
  <!-- Gischt am Steven -->
  <g class="far" stroke-dasharray="3 7" opacity=".5">
    <path d="M96 330 C 76 312, 62 300, 44 294"/>
    <path d="M112 316 C 98 296, 88 284, 76 274"/>
  </g>
'''


def ring(cx, cy, r, sw=1.6):
    out = ['<circle cx="%g" cy="%g" r="%g" fill="none" stroke="#1d4f37" '
           'stroke-width="%g" opacity=".5"/>' % (cx, cy, r, sw)]
    for d in range(0, 360, 15):
        major = (d % 45 == 0)
        ri = r - r * (0.055 if major else 0.032)
        a = math.radians(d)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                   'stroke-width="%g" opacity="%s"/>'
                   % (cx + ri*math.sin(a), cy - ri*math.cos(a),
                      cx + r*math.sin(a), cy - r*math.cos(a),
                      '#7d6a2a' if major else '#2f9d6b',
                      sw*1.4 if major else sw*0.9,
                      '.45' if major else '.28'))
    return '\n'.join(out)


def waves(W, rows):
    return '\n'.join(
        '<path d="%s" fill="none" stroke="#63f0a0" stroke-linecap="round" '
        'stroke-width="%g" stroke-dasharray="%s" opacity="%s"/>' % (d, w, da, op)
        for d, w, da, op in rows)


TPL = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;background:#070b0e}}svg{{display:block}}</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="ng" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.6" result="b2"/>
    <feGaussianBlur stdDeviation="0.9" result="b1"/>
    <feMerge><feMergeNode in="b2"/><feMergeNode in="b2"/>
      <feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <radialGradient id="sky" cx="{gx}%" cy="8%" r="94%">
    <stop offset="0%" stop-color="#182731"/>
    <stop offset="56%" stop-color="#0b1014"/>
    <stop offset="100%" stop-color="#060a0d"/>
  </radialGradient>
  <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">
    <rect width="4" height="1.1" fill="#000" opacity=".3"/>
  </pattern>
  <style>
    .near {{ fill:none; stroke:#7dffb8; stroke-width:3.4; stroke-linecap:round; stroke-linejoin:round; }}
    .mid  {{ fill:none; stroke:#7dffb8; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
    .far  {{ fill:none; stroke:#63f0a0; stroke-width:1.4; stroke-linecap:round; stroke-linejoin:round; }}
    .wire {{ fill:none; stroke:#63f0a0; stroke-width:1.2; stroke-linecap:round; }}
    .deep {{ fill:none; stroke:#2f9d6b; stroke-width:1.5; stroke-linecap:round; opacity:.7; }}
  </style>
</defs>

<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g>{RING}</g>
<g filter="url(#ng)" opacity=".5">{FAR}</g>
<g transform="translate({tx} {ty}) scale({s})"><g filter="url(#ng)">{BOOT}</g></g>
<g filter="url(#ng)" opacity=".55">{NEAR}</g>
<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".5" style="mix-blend-mode:overlay"/>
<rect x="1.5" y="1.5" width="{Wi}" height="{Hi}" rx="10" fill="none" stroke="#1d4f37" stroke-width="1.5"/>
</svg></body></html>'''


def build(name, W, H, s, tx, ty, rc, rr, far, near, gx=44):
    io.open(name, 'w', encoding='utf-8').write(TPL.format(
        W=W, H=H, s=s, tx=tx, ty=ty, gx=gx,
        RING=ring(rc[0], rc[1], rr), FAR=waves(W, far), NEAR=waves(W, near),
        BOOT=BOOT, Wi=W-3, Hi=H-3))
    print('%s  %dx%d' % (name, W, H))


# ---- breit: 960x420, mit Faktor 2 -> 1920x840 -------------------------------
build('_ub-wide.html', 960, 420, 0.80, 78, 46, (500, 214), 196,
      [('M0 128 H960', 1.1, '3 52', '.16'),
       ('M0 146 H960', 1.2, '4 42', '.20'),
       ('M0 168 H960', 1.2, '6 34', '.24')],
      [('M0 246 C 140 240, 300 250, 460 252 C 640 254, 820 246, 960 240', 1.3, '9 26', '.16'),
       ('M0 290 C 160 282, 340 296, 500 300 C 680 304, 830 294, 960 286', 1.5, '12 22', '.20'),
       ('M0 344 C 180 334, 380 352, 560 356 C 740 360, 860 348, 960 340', 1.7, '16 18', '.26'),
       ('M0 398 C 200 386, 420 406, 620 410 C 790 413, 880 402, 960 394', 1.9, '20 16', '.30')])

# ---- quadratisch: 500x500, mit Faktor 2 -> 1000x1000 ------------------------
build('_ub-square.html', 500, 500, 0.52, 2, 128, (250, 250), 206,
      [('M0 96 H500',  1.0, '3 46', '.14'),
       ('M0 112 H500', 1.1, '4 38', '.18'),
       ('M0 132 H500', 1.1, '5 30', '.22')],
      [('M0 296 C 80 290, 170 300, 250 302 C 350 305, 430 298, 500 293', 1.3, '9 24', '.18'),
       ('M0 334 C 90 326, 190 340, 280 344 C 380 348, 440 338, 500 332', 1.5, '12 20', '.22'),
       ('M0 382 C 100 372, 220 390, 320 394 C 410 397, 460 386, 500 380', 1.7, '15 17', '.26'),
       ('M0 434 C 120 422, 250 442, 360 446 C 440 449, 470 438, 500 432', 1.9, '19 15', '.30')],
      gx=40)
