# -*- coding: utf-8 -*-
"""Typ VII/C als 3D-Drahtmodell in Metern, echte Zentralprojektion.

Kamera steht still. Das Boot kommt entgegen und laeuft links vorbei:
Bug nah und links unten, Rumpf verkuerzt sich nach rechts hinten zum Horizont.
"""
import io, math

# ---------------------------------------------------------------- Rumpfdaten
# x = Laengsachse in Metern, 0 = Bug, 67.1 = Heck (Typ VII/C)
XS = [0,   3,   6,   10,  15,  22,  30,  40,  48,  55,  60,  64,  67]
WD = [0,  1.0, 1.5, 1.9, 2.1, 2.2, 2.2, 2.2, 2.1, 1.8, 1.3, 0.7, 0]   # Deckskasten, halbe Breite
ZD = [3.4, 3.0, 2.7, 2.45,2.25,2.1, 2.0, 1.95,1.9, 1.8, 1.65,1.4, 1.2] # Deckshoehe ueber Wasser
WH = [0,  1.6, 2.4, 3.0, 3.3, 3.45,3.45,3.4, 3.2, 2.8, 2.1, 1.1, 0]   # Rumpf an der Wasserlinie

def lerp(xs, ys, x):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    for i in range(len(xs)-1):
        if xs[i] <= x <= xs[i+1]:
            t = (x-xs[i])/(xs[i+1]-xs[i])
            return ys[i] + t*(ys[i+1]-ys[i])
    return ys[-1]

wd = lambda x: lerp(XS, WD, x)
zd = lambda x: lerp(XS, ZD, x)
wh = lambda x: lerp(XS, WH, x)

# Stevenfall des VII/C: das Deck ragt am Bug ueber, der Vorfuss liegt zurueck.
import math as _m
def xd(x):   return x - 1.5*_m.exp(-x/2.6)      # Deckskante nach vorn versetzt
def xw(x):   return x + 1.3*_m.exp(-x/2.2)      # Wasserlinie nach achtern versetzt

# ---------------------------------------------------------------- Kamera
import sys
PRESET = sys.argv[1] if len(sys.argv) > 1 else 'tele'
if PRESET == 'quadrat':      # Markenbild 500x500
    W, H = 500, 500
    CX, CY, F, EYE, PHI, BX, BY = 285.0, 215.0, 700.0, 5.0, math.radians(25), -10.5, 33.0
    RING = (250, 250, 200)
    SEA_F, SEA_N = (400, 220, 130), (52, 34, 25, 19.5, 15.5)
elif PRESET == 'tele':       # Teleperspektive
    W, H = 960, 420
    CX, CY, F, EYE, PHI, BX, BY = 452.0, 176.0, 3000.0, 5.0, math.radians(32), -14.4, 130.0
    RING = (452, 200, 188)
    SEA_F, SEA_N = (1600, 900, 560), (240, 132, 82, 55)
else:                        # nah, kurze Brennweite - die gewaehlte Fassung
    W, H = 960, 420
    CX, CY, F, EYE, PHI, BX, BY = 560.0, 176.0, 900.0, 5.0, math.radians(25), -13.0, 33.0
    RING = (474, 200, 188)
    SEA_F, SEA_N = (400, 220, 130), (48, 32, 24, 19)

SIN, COS = math.sin(PHI), math.cos(PHI)

def proj(x, a, z):
    """Bootskoordinaten (x laengs ab Bug, a nach Backbord, z ueber Wasser) -> Bild."""
    wx = BX + x*SIN + a*COS
    wy = BY + x*COS - a*SIN
    dz = z - EYE
    return (CX + F*wx/wy, CY - F*dz/wy)

def path(pts, close=False):
    d = 'M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p for p in pts[1:])
    return d + (' Z' if close else '')

def curve(fn, x0, x1, n=26):
    return [proj(*fn(x0 + (x1-x0)*i/float(n))) for i in range(n+1)]

# ---------------------------------------------------------------- Bauteile
P = []   # (klasse, strichmuster, extra, d)
def add(cls, dash, d, extra=''):
    P.append('<path class="%s" stroke-dasharray="%s" %s d="%s"/>' % (cls, dash, extra, d))

# Deckskante Backbord (uns zugewandt) und Steuerbord (abgewandt)
add('near', '13 8', path(curve(lambda x: (xd(x),  wd(x), zd(x)), 0, 67)))
add('mid',  '9 8',  path(curve(lambda x: (xd(x), -wd(x), zd(x)), 0, 67)), 'opacity=".72"')

# Wasserlinie Backbord, dazu ein Stueck Steuerbord am Bug
add('near', '14 8', path(curve(lambda x: (xw(x),  wh(x), 0), 0, 67)))
add('far',  '6 8',  path(curve(lambda x: (xw(x), -wh(x), 0), 0, 11)), 'opacity=".5"')

# Steven: senkrechte Kante am Bug
add('near', '9 6', path([proj(xw(0), 0, 0), proj(0.35, 0, 0.9), proj(-0.55, 0, 1.9),
                         proj(-1.15, 0, 2.7), proj(xd(0), 0, 3.4)]))

# Satteltankwulst, knapp unter der Oberflaeche
add('deep', '5 9', path(curve(lambda x: (x, wh(x)*1.06, -0.55), 3, 62)), 'opacity=".42"')

# Spanten: Deckskante -> Bordwand -> Wasserlinie
sp = []
for x in (8, 14, 21, 29, 38, 46, 54, 60):
    sp.append(path([proj(x, wd(x), zd(x)),
                    proj(x, wh(x)*0.99, zd(x)*0.45),
                    proj(x, wh(x), 0)]))
P.append('<g class="deep" stroke-dasharray="3 6" opacity=".7">%s</g>'
         % ''.join('<path d="%s"/>' % s for s in sp))

# Decksluken laengs
lu = []
for x0, x1 in ((7, 12), (16, 21), (26, 31), (50, 55)):
    lu.append(path([proj(x0, wd(x0)*0.45, zd(x0)+0.05),
                    proj(x1, wd(x1)*0.45, zd(x1)+0.05)]))
P.append('<g class="far" stroke-dasharray="2 5" opacity=".45">%s</g>'
         % ''.join('<path d="%s"/>' % s for s in lu))

# Deckgeschuetz 8,8 cm bei x = 24
gx = 24.0
add('mid', '4 4', path([proj(gx, 0.7, zd(gx)), proj(gx, 0.7, zd(gx)+0.75),
                        proj(gx, -0.7, zd(gx)+0.75), proj(gx, -0.7, zd(gx))]))
add('mid', '4 4', path([proj(gx-0.3, 0, zd(gx)+0.7), proj(gx-4.6, 0, zd(gx)+1.35)]))

# ---- Turm: ovaler Grundriss, kleiner als vorher
xc, tl, tb, tz = 37.6, 3.1, 1.35, 6.5
zt = zd(xc)
def tp(t, z):                      # Punkt auf dem Turmoval
    return proj(xc + tl*math.cos(t), tb*math.sin(t), z)

N = 30
oben = [tp(2*math.pi*i/N, tz) for i in range(N+1)]
add('mid', '7 5', path(oben), 'opacity=".9"')
bb_o = [tp(math.pi*i/16, tz) for i in range(17)]      # Backbordhaelfte oben
bb_u = [tp(math.pi*i/16, zt) for i in range(17)]      # Backbordhaelfte unten
add('near', '10 6', path(bb_u))
add('near', '9 6', path([bb_o[0], bb_u[0]]))
add('near', '9 6', path([bb_o[-1], bb_u[-1]]))
# Bruestung
add('far', '3 4', path([tp(math.pi*i/16, tz-0.75) for i in range(17)]), 'opacity=".6"')

# ---- Wintergarten, rund, achtern am Turm
w0, wb, wz = xc + tl - 0.3, 1.15, tz - 1.05
wg = [proj(w0 + 2.6*math.sin(math.pi*i/14), wb*math.cos(math.pi*i/14 - math.pi/2)*1.0, wz)
      for i in range(15)]
add('mid', '5 5', path(wg))
add('far', '2.5 4', path([proj(w0 + 2.6*math.sin(math.pi*i/14),
                              wb*math.cos(math.pi*i/14 - math.pi/2), wz - 0.55)
                          for i in range(15)]), 'opacity=".55"')
rl = [path([proj(w0 + 2.6*math.sin(math.pi*i/7), wb*math.cos(math.pi*i/7 - math.pi/2), wz-0.55),
            proj(w0 + 2.6*math.sin(math.pi*i/7), wb*math.cos(math.pi*i/7 - math.pi/2), wz)])
      for i in range(8)]
P.append('<g class="far" stroke-dasharray="2 3" opacity=".5">%s</g>'
         % ''.join('<path d="%s"/>' % r for r in rl))

# ---- Sehrohre, Peilrahmen, Antennenmast
add('mid', '4 4', path([proj(36.9, 0.35, tz), proj(36.9, 0.35, 10.2)]))
add('mid', '4 4', path([proj(38.6, -0.35, tz), proj(38.6, -0.35, 9.1)]))
add('far', '2.5 4', path([proj(39.9, 0.7, tz), proj(39.9, 0.7, 8.4)]), 'opacity=".7"')
add('far', '2.5 4', path([proj(36.9, -0.8, 8.9), proj(36.9, 1.5, 8.9)]), 'opacity=".7"')
bx, by = proj(38.6, -0.35, 9.1)
P.append('<circle cx="%.1f" cy="%.1f" r="4" class="far" stroke-dasharray="2.2 2.2"/>' % (bx, by))

# ---- Netzabweiser
add('wire', '2.5 6', path([proj(xd(0), 0, 3.4), proj(xc-tl+0.2, 0, tz-0.3)]), 'opacity=".8"')
add('wire', '2.5 6', path([proj(w0+2.4, 0, wz-0.4), proj(66.4, 0, 1.4)]), 'opacity=".8"')

# ---------------------------------------------------------------- Bugsee
bw = []
for off, op, dash, cls in ((1.5, '.85', '11 7', 'near'),
                           (3.2, '.6',  '8 9',  'mid'),
                           (5.4, '.38', '6 11', 'far')):
    pts = [proj(xw(x), wh(x) + off + 0.16*x, 0.75*math.exp(-x/9.0))
           for x in [1,3,6,10,15,21,28,36,45]]
    bw.append('<path class="%s" stroke-dasharray="%s" opacity="%s" d="%s"/>'
              % (cls, dash, op, path(pts)))
# brechender Kamm vor dem Steven
bw.append('<path class="near" stroke-dasharray="8 6" opacity=".85" d="%s"/>' % path(
    [proj(-6.0, -1.8, 0.2), proj(-3.8, 1.2, 1.1), proj(-1.4, 4.2, 1.4),
     proj(1.4, 7.2, 0.9), proj(4.6, 9.6, 0.35)]))
bw.append('<path class="mid" stroke-dasharray="5 8" opacity=".5" d="%s"/>' % path(
    [proj(-9.5, -3.4, 0.15), proj(-6.0, 0.4, 0.7), proj(-2.4, 5.4, 0.95),
     proj(1.8, 10.0, 0.5), proj(6.4, 13.2, 0.15)]))
P.append(''.join(bw))

# ---- Heck: Deckskante und Wasserlinie laufen in der Spitze zusammen
add('near', '6 5', path([proj(67, 0, zd(67)), proj(67.3, 0, 0.6), proj(xw(67), 0, 0)]))

# ---- Achterschiff: Auslauf und Ruderblatt
add('mid', '7 6', path([proj(60, wd(60), zd(60)), proj(64, wd(64)*0.8, zd(64)),
                        proj(67, 0, 1.2)]), 'opacity=".85"')
add('far', '4 6', path([proj(62, 0, 0.9), proj(66.5, 0, 0.7), proj(67.4, 0, -0.9)]),
    'opacity=".6"')

# ---------------------------------------------------------------- Kielwasser
kw = []
for sgn, op, dash in ((1, '.3', '11 12'), (-1, '.3', '11 12'),
                      (1, '.16', '7 16'), (-1, '.16', '7 16')):
    spread = 1.6 if abs(op == '.4') else 3.4
    pts = [proj(67 + i*9.0, sgn*(1.2 + i*(2.2 if op == '.4' else 4.0)), 0)
           for i in range(10)]
    kw.append('<path class="far" stroke-dasharray="%s" opacity="%s" d="%s"/>'
              % (dash, op, path(pts)))
P.append(''.join(kw))

# ---------------------------------------------------------------- Seegang
def sealine(dist, dash, op, w):
    """Waagerechte Duenung in echter Entfernung -> richtige Perspektive."""
    pts = []
    for i in range(41):
        wx = -0.62*dist + 1.24*dist*i/40.0
        pts.append((CX + F*wx/dist, CY + F*EYE/dist + 5.0*math.sin(i*0.9 + dist)))
    return ('<path class="sea" stroke-width="%g" stroke-dasharray="%s" opacity="%s" d="%s"/>'
            % (w, dash, op, path(pts)))

DASH_F = (('3 40', '.16', 1.1), ('4 34', '.2', 1.2), ('6 28', '.24', 1.3))
DASH_N = (('10 24', '.2', 1.5), ('14 20', '.24', 1.7),
          ('18 16', '.28', 1.9), ('24 14', '.3', 2.1), ('28 12', '.3', 2.2))
FERN = ''.join(sealine(d, *DASH_F[i]) for i, d in enumerate(SEA_F))
NAH  = ''.join(sealine(d, *DASH_N[i]) for i, d in enumerate(SEA_N))

SVG = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{margin:0;background:#070b0e}svg{display:block}</style></head><body>
<svg width="%(W)d" height="%(H)d" viewBox="0 0 %(W)d %(H)d" xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="ng" x="-40%%" y="-40%%" width="180%%" height="180%%">
    <feGaussianBlur stdDeviation="2.6" result="b2"/><feGaussianBlur stdDeviation="0.9" result="b1"/>
    <feMerge><feMergeNode in="b2"/><feMergeNode in="b2"/>
      <feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <radialGradient id="sky" cx="46%%" cy="12%%" r="94%%">
    <stop offset="0%%" stop-color="#182731"/><stop offset="56%%" stop-color="#0b1014"/>
    <stop offset="100%%" stop-color="#060a0d"/>
  </radialGradient>
  <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">
    <rect width="4" height="1.1" fill="#000" opacity=".3"/></pattern>
  <style>
    .near {stroke:#7dffb8; stroke-width:3.0}
    .mid  {stroke:#7dffb8; stroke-width:2.1}
    .far  {stroke:#63f0a0; stroke-width:1.4}
    .wire {stroke:#63f0a0; stroke-width:1.1}
    .deep {stroke:#2f9d6b; stroke-width:1.4}
    .sea  {stroke:#63f0a0}
    path, circle {fill:none; stroke-linecap:round; stroke-linejoin:round}
  </style>
</defs>
<rect width="%(W)d" height="%(H)d" fill="url(#sky)"/>
<circle cx="%(rx)g" cy="%(ry)g" r="%(rr)g" fill="none" stroke="#1d4f37" stroke-width="1.6" opacity=".45"/>
<g filter="url(#ng)" opacity=".5">%(FERN)s</g>
<g filter="url(#ng)">%(BOOT)s</g>
<g filter="url(#ng)" opacity=".55">%(NAH)s</g>
<rect width="%(W)d" height="%(H)d" fill="url(#scan)" opacity=".5" style="mix-blend-mode:overlay"/>
<rect x="1.5" y="1.5" width="%(Wi)d" height="%(Hi)d" rx="10" fill="none" stroke="#1d4f37" stroke-width="1.5"/>
</svg></body></html>''' % {'BOOT': ''.join(P), 'FERN': FERN, 'NAH': NAH, 'rx': RING[0], 'ry': RING[1], 'rr': RING[2],
           'W': W, 'H': H, 'Wi': W-3, 'Hi': H-3}

io.open('_v3d.html', 'w', encoding='utf-8').write(SVG)

b = proj(0, 0, 0); s = proj(67, 0, 0); t = proj(36.5, 0.4, 13.2)
print('Bug   %6.1f %6.1f' % b)
print('Heck  %6.1f %6.1f' % s)
print('Mast  %6.1f %6.1f' % t)
print('Horizont y = %.1f' % CY)
