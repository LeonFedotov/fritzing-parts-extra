# Generates the Hardkernel ODROID-SHOW2 Fritzing part (front view, as in
# Hardkernel's board photo) from the dimensioned board render (dimension2.png,
# measured: it is the front rotated 180 degrees), the rev 0.1 schematic and
# the Tianma TM022HDH26 LCD datasheet.
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'odroid-show2') + '/'
os.makedirs(OUT, exist_ok=True)
W, H = 83.0, 48.0
PCB, PCB_EDGE, SILK, GOLD, RING = '#23607a', '#163f50', '#f2f2ee', '#d6b052', '#9c7a2a'
FONT = "font-family='OCRA, Droid Sans Mono, monospace'"
P = 2.54

def f(v): return f'{v:.3f}'

# connectors: (name, description, x, y, kind)
CON = []
for name, desc, y in [('GND', 'P2 pin 6, ground', 25.20), ('INT0', 'P2 pin 5, PD2 / D2 (INT0)', 25.20 + P),
                      ('ADC3', 'P2 pin 4, PC3 / A3', 25.20 + 2 * P), ('SDA', 'P2 pin 3, PC4 / A4 (I2C SDA)', 25.20 + 3 * P),
                      ('SCL', 'P2 pin 2, PC5 / A5 (I2C SCL)', 25.20 + 4 * P), ('P3V45', 'P2 pin 1, 3.45 V supply', 25.20 + 5 * P)]:
    CON.append((name, desc, 3.10, y, 'pin'))
for name, desc, x, y in [('MISO', 'ISP pin 1, PB4 / D12', 2.88, 11.55), ('P3V45', 'ISP pin 2, 3.45 V', 2.88, 9.01),
                         ('SCK', 'ISP pin 3, PB5 / D13', 5.42, 11.55), ('MOSI', 'ISP pin 4, PB3 / D11', 5.42, 9.01),
                         ('RESET', 'ISP pin 5, MCU reset', 7.96, 11.55), ('GND', 'ISP pin 6, ground', 7.96, 9.01)]:
    CON.append((name, desc, x, y, 'pin'))
CON.append(('DTR', 'P1 pin 1, CP2104 DTR: fit the jumper to reset from USB serial', 17.96, 1.86, 'pin'))
CON.append(('RESET_C', 'P1 pin 2, to RESET through 0.1 uF', 17.96, 4.40, 'pin'))
CON.append(('BAT+', 'battery connector +, LiPo 3.7 V (charged at 4.2 V, 500 mA)', 1.0, 16.65, 'wire'))
CON.append(('BAT-', 'battery connector -, ground', 1.0, 18.65, 'wire'))

def outline_path():
    r, nr = 2.5, 1.5            # corner, notch-corner radius
    nx, n0, n1 = 76.0, 8.5, 33.5  # notch: inner edge x, top y, bottom y (right side)
    return (f"M{r},0 H{W - r} A{r},{r} 0 0 1 {W},{r} V{n0 - nr} A{nr},{nr} 0 0 1 {W - nr},{n0} H{nx + nr} "
            f"A{nr},{nr} 0 0 0 {nx},{n0 + nr} V{n1 - nr} A{nr},{nr} 0 0 0 {nx + nr},{n1} H{W - nr} "
            f"A{nr},{nr} 0 0 1 {W},{n1 + nr} V{H - r} A{r},{r} 0 0 1 {W - r},{H} H{r} A{r},{r} 0 0 1 0,{H - r} V{r} A{r},{r} 0 0 1 {r},0 Z")

def chip(x, y, w, h, pins_per_side, label=None, quad=True, dot='tl'):
    s = [f"<rect x='{f(x)}' y='{f(y)}' width='{f(w)}' height='{f(h)}' rx='0.2' fill='#2b2b2b' stroke='#111' stroke-width='0.08'/>"]
    if quad:
        for i in range(pins_per_side):
            t = (i + 0.5) / pins_per_side
            px, py = x + t * w, y + t * h
            s += [f"<rect x='{f(px - 0.15)}' y='{f(y - 0.7)}' width='0.3' height='0.7' fill='#bfbfbf'/>",
                  f"<rect x='{f(px - 0.15)}' y='{f(y + h)}' width='0.3' height='0.7' fill='#bfbfbf'/>",
                  f"<rect x='{f(x - 0.7)}' y='{f(py - 0.15)}' width='0.7' height='0.3' fill='#bfbfbf'/>",
                  f"<rect x='{f(x + w)}' y='{f(py - 0.15)}' width='0.7' height='0.3' fill='#bfbfbf'/>"]
    dx = x + 0.7 if dot[1] == 'l' else x + w - 0.7
    dy = y + 0.7 if dot[0] == 't' else y + h - 0.7
    s.append(f"<circle cx='{f(dx)}' cy='{f(dy)}' r='0.25' fill='#555'/>")
    if label:
        s.append(f"<text x='{f(x + w / 2)}' y='{f(y + h / 2 + 0.35)}' {FONT} font-size='0.9' fill='#9a9a9a' text-anchor='middle'>{label}</text>")
    return s

def passives():
    # a few 0603 parts where the render has them (approximate), for the board's look
    s = []
    for x, y, rot in [(9.5, 16.8, 0), (11.0, 16.8, 0), (16.6, 21.0, 90), (17.4, 30.5, 0), (14.0, 31.0, 0), (9.0, 19.5, 90),
                      (6.0, 6.0, 0), (17.0, 11.0, 90), (13.0, 17.5, 0), (15.5, 8.0, 0), (19.0, 12.5, 90), (8.8, 13.6, 0)]:
        w, h = (1.6, 0.8) if rot == 0 else (0.8, 1.6)
        s += [f"<rect x='{f(x - w / 2)}' y='{f(y - h / 2)}' width='{w}' height='{h}' fill='#c9c3b6'/>",
              f"<rect x='{f(x - w / 2 + (0.3 if rot == 0 else 0))}' y='{f(y - h / 2 + (0 if rot == 0 else 0.3))}' width='{f(w - 0.6 if rot == 0 else w)}' height='{f(h if rot == 0 else h - 0.6)}' fill='#6b5d4f'/>"]
    return s

def header(xs_ys, pitch_box):
    x0, y0, x1, y1 = pitch_box
    s = [f"<rect x='{f(x0)}' y='{f(y0)}' width='{f(x1 - x0)}' height='{f(y1 - y0)}' rx='0.2' fill='#262722' stroke='#111' stroke-width='0.08'/>"]
    return s

def breadboard():
    s = ["<?xml version='1.0' encoding='UTF-8'?>",
         "<!-- Hardkernel ODROID-SHOW2, front view. Outline, holes, connectors and parts measured from Hardkernel's",
         "     dimensioned board render; LCD from the Tianma TM022HDH26 datasheet; pins from the rev 0.1 schematic. -->",
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{W / 25.4:.5f}in' height='{H / 25.4:.5f}in' viewBox='0 0 {W} {H}'>",
         "<g id='breadboard'>",
         f"<path d='{outline_path()}' fill='{PCB}' stroke='{PCB_EDGE}' stroke-width='0.2'/>"]
    # mounting holes, 3 mm, plated
    for x, y in [(3.4, 3.4), (79.6, 3.4), (3.4, 44.6), (79.6, 44.6)]:
        s.append(f"<circle cx='{x}' cy='{y}' r='2.6' fill='{GOLD}' stroke='{RING}' stroke-width='0.1'/><circle cx='{x}' cy='{y}' r='1.6' fill='#ffffff' fill-opacity='0.85'/>")
    # LCD module: white frame, dark glass, active area
    s.append("<rect x='20.45' y='0.85' width='55.2' height='40.1' rx='0.6' fill='#e3e4dc' stroke='#b9bab2' stroke-width='0.15'/>")
    s.append("<rect x='21.3' y='2.5' width='53.2' height='36.8' rx='0.3' fill='#0f0e0c'/>")
    s.append("<rect x='25.34' y='3.98' width='45.12' height='33.84' fill='#171a1d'/>")
    s.append(f"<text x='47.9' y='21.6' {FONT} font-size='1.6' fill='#2c3136' text-anchor='middle'>2.2 in 320 x 240 TFT</text>")
    # ICs, crystal, passives
    s += chip(8.6, 21.0, 7.0, 7.0, 8, 'ATMEGA328P', dot='bl')  # U1, TQFP-32: pin 1 at the bottom-left corner, pins 1-8 along the bottom
    s += chip(12.0, 11.6, 4.0, 4.0, 6, 'CP2104', dot='tr')  # U2, QFN-24
    s += chip(16.0, 6.4, 1.5, 3.0, 0, None, quad=False)    # U3 charger
    s.append("<rect x='6.2' y='33.1' width='11.9' height='5.0' rx='1.2' fill='#c8c8c8' stroke='#8a8a8a' stroke-width='0.1'/>")
    s.append(f"<text x='12.15' y='36.0' {FONT} font-size='1.2' fill='#555' text-anchor='middle'>16.000</text>")
    s += passives()
    # micro USB (overhangs the top edge), power switch, reset, LEDs, buttons
    s.append("<rect x='7.8' y='-0.6' width='7.5' height='6.1' rx='0.4' fill='#b8b8b8' stroke='#7a7a7a' stroke-width='0.12'/>")
    s.append("<rect x='9.0' y='0.4' width='5.1' height='1.4' rx='0.3' fill='#3a3a3a'/>")
    s.append("<rect x='7.0' y='40.6' width='9.4' height='5.5' rx='0.3' fill='#5e564e' stroke='#3a352f' stroke-width='0.1'/>")
    s.append("<rect x='12.2' y='41.6' width='2.6' height='2.2' fill='#d8d8d8'/>")
    s.append(f"<text x='7.4' y='39.9' {FONT} font-size='0.9' fill='{SILK}'>OFF</text><text x='14.4' y='39.9' {FONT} font-size='0.9' fill='{SILK}'>ON</text>")
    s.append("<rect x='22.3' y='42.2' width='4.0' height='4.0' rx='0.3' fill='#c0c0c0' stroke='#888' stroke-width='0.1'/><circle cx='24.3' cy='44.2' r='1.15' fill='#2a2a2a'/>")
    s.append(f"<text x='24.3' y='41.6' {FONT} font-size='0.8' fill='{SILK}' text-anchor='middle'>RESET</text>")
    for x, color, label in [(31.3, '#e8463b', 'PD3'), (35.5, '#3fbf5a', 'PD4'), (39.7, '#3b7be8', 'PD6')]:
        s.append(f"<rect x='{f(x - 0.8)}' y='44.9' width='1.6' height='0.8' fill='{color}' stroke='#555' stroke-width='0.05'/>")
        s.append(f"<text x='{f(x)}' y='44.3' {FONT} font-size='0.75' fill='{SILK}' text-anchor='middle'>{label}</text>")
    for x, label in [(48.6, 'PD7'), (57.2, 'PC0'), (65.8, 'PC1')]:
        s.append(f"<rect x='{f(x - 3.0)}' y='44.2' width='6.0' height='3.5' rx='0.3' fill='#dedac8' stroke='#9a978a' stroke-width='0.1'/>")
        s.append(f"<rect x='{f(x - 1.2)}' y='44.9' width='2.4' height='2.1' rx='0.4' fill='#bdb9a8'/>")
        s.append(f"<text x='{f(x)}' y='43.5' {FONT} font-size='0.8' fill='{SILK}' text-anchor='middle'>{label}</text>")
    # charge LED D4 (green, lit while charging)
    s.append("<rect x='6.9' y='14.6' width='1.6' height='0.8' fill='#3fbf5a' stroke='#555' stroke-width='0.05'/>")
    # headers: ISP 2x3, P1 2-pin, P2 6-pin, battery connector
    s.append("<rect x='1.61' y='7.74' width='7.62' height='5.08' rx='0.2' fill='#262722'/>")
    s.append("<rect x='16.69' y='0.59' width='2.54' height='5.08' rx='0.2' fill='#262722'/>")
    s.append("<rect x='1.83' y='23.93' width='2.54' height='15.24' rx='0.2' fill='#444f50'/>")
    s.append("<rect x='1.0' y='14.6' width='4.6' height='7.8' rx='0.3' fill='#e9e1c8' stroke='#b5a983' stroke-width='0.12'/>")
    s.append("<rect x='1.0' y='15.6' width='1.2' height='4.1' fill='#c8b78d'/>")
    s.append(f"<text transform='translate(6.9,18.5) rotate(90)' {FONT} font-size='0.8' fill='{SILK}' text-anchor='middle'>BATTERY</text>")
    s.append(f"<text x='1.6' y='14.1' {FONT} font-size='0.8' fill='{SILK}'>+</text>")
    s.append(f"<text x='5.3' y='7.2' {FONT} font-size='0.8' fill='{SILK}' text-anchor='middle'>ISP</text>")
    s.append(f"<text x='16.3' y='3.4' {FONT} font-size='0.75' fill='{SILK}' text-anchor='end'>DTR</text>")
    s.append(f"<text x='3.1' y='23.4' {FONT} font-size='0.8' fill='{SILK}' text-anchor='middle'>P2</text>")
    for i, (name, _, x, y, kind) in enumerate(CON):
        if kind == 'wire':
            s.append(f"<rect id='connector{i}pin' x='{f(x - 0.4)}' y='{f(y - 0.4)}' width='0.8' height='0.8' fill='{GOLD}'/>")
            continue
        s.append(f"<circle id='connector{i}pin' cx='{f(x)}' cy='{f(y)}' r='0.85' fill='{GOLD}' stroke='{RING}' stroke-width='0.1'/>")
        s.append(f"<rect x='{f(x - 0.32)}' y='{f(y - 0.32)}' width='0.64' height='0.64' fill='#8c8c8c'/>")
        if i < 6:  # P2 labels, as on the silkscreen
            s.append(f"<text x='4.55' y='{f(y + 0.3)}' {FONT} font-size='0.8' fill='{SILK}'>{name}</text>")
    s += ["</g>", "</svg>", ""]
    return '\n'.join(s)

def schematic():
    lp = ['P3V45', 'GND', 'BAT+', 'BAT-', 'DTR', 'RESET_C']
    rp = ['INT0', 'ADC3', 'SDA', 'SCL', 'MISO', 'MOSI', 'SCK', 'RESET']
    ids = {}
    for i, (name, *_rest) in enumerate(CON):
        ids.setdefault(name, []).append(i)
    used = {k: 0 for k in ids}
    def cid(name):
        i = ids[name][used[name]]; used[name] += 1; return i
    # power and ground pins appear twice (P2 and ISP): list the second ones too
    lp += ['P3V45', 'GND']
    pitch, pl, w = 10, 10, 90
    h = pitch * (max(len(lp), len(rp)) + 1)
    s = ["<?xml version='1.0' encoding='UTF-8'?>",
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{(w + 2 * pl) / 100:.2f}in' height='{h / 100:.2f}in' viewBox='0 0 {w + 2 * pl} {h}'>",
         "<g id='schematic'>",
         f"<rect x='{pl}' y='0' width='{w}' height='{h}' fill='none' stroke='#000' stroke-width='1'/>",
         f"<text x='{pl + w / 2}' y='7' font-family='Droid Sans' font-size='7' text-anchor='middle'>ODROID-SHOW2</text>"]
    for side, pins in (('l', lp), ('r', rp)):
        for k, name in enumerate(pins):
            y = (k + 1) * pitch + (2 if k == 0 else 0) * 0
            i = cid(name)
            x0 = 0 if side == 'l' else pl + w
            s.append(f"<line id='connector{i}pin' x1='{x0}' y1='{y}' x2='{x0 + pl}' y2='{y}' stroke='#000' stroke-width='1'/>")
            tx = x0 if side == 'l' else x0 + pl - 1
            s.append(f"<rect id='connector{i}terminal' x='{tx}' y='{y - 0.5}' width='1' height='1' fill='none'/>")
            lx = pl + 2 if side == 'l' else pl + w - 2
            s.append(f"<text x='{lx}' y='{y + 2.5}' font-family='Droid Sans' font-size='7' text-anchor='{'start' if side == 'l' else 'end'}'>{name}</text>")
    s += ["</g>", "</svg>", ""]
    return '\n'.join(s)

def pcb():
    s = ["<?xml version='1.0' encoding='UTF-8'?>",
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{W / 25.4:.5f}in' height='{H / 25.4:.5f}in' viewBox='0 0 {W} {H}'>",
         f"<g id='silkscreen'><path d='{outline_path()}' fill='none' stroke='#000' stroke-width='0.15'/></g>"]
    for layer in ('copper0', 'copper1'):
        s.append(f"<g id='{layer}'>")
        for i, (name, _, x, y, kind) in enumerate(CON):
            if kind == 'wire':
                if layer == 'copper1':
                    s.append(f"<rect id='connector{i}pad' x='{f(x - 0.5)}' y='{f(y - 0.5)}' width='1' height='1' fill='#F7BD13'/>")
                continue
            s.append(f"<circle id='connector{i}pad' cx='{f(x)}' cy='{f(y)}' r='0.65' fill='none' stroke='#F7BD13' stroke-width='0.5'/>")
        s.append("</g>")
    s += ["</svg>", ""]
    return '\n'.join(s)

def fzp(stem):
    cons = []
    for i, (name, desc, x, y, kind) in enumerate(CON):
        pcbv = (f"<p layer='copper1' svgId='connector{i}pad'/>" if kind == 'wire' else
                f"<p layer='copper0' svgId='connector{i}pad'/><p layer='copper1' svgId='connector{i}pad'/>")
        cons.append(f"""  <connector id='connector{i}' name='{name}' type='{'pad' if kind == 'wire' else 'female'}'>
   <description>{desc}</description>
   <views>
    <breadboardView><p layer='breadboard' svgId='connector{i}pin'/></breadboardView>
    <schematicView><p layer='schematic' svgId='connector{i}pin' terminalId='connector{i}terminal'/></schematicView>
    <pcbView>{pcbv}</pcbView>
   </views>
  </connector>""")
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<module fritzingVersion='1.0.0' moduleId='HardkernelOdroidShow2ModuleID'>
 <version>1</version>
 <title>ODROID-SHOW2</title>
 <label>U</label>
 <date>2026-10-06</date>
 <author>fritzing-parts-extra, from Hardkernel's published board drawing and schematic</author>
 <tags><tag>Hardkernel</tag><tag>ODROID</tag><tag>SHOW2</tag><tag>ATmega328P</tag><tag>TFT</tag><tag>LCD</tag><tag>Arduino</tag></tags>
 <properties>
  <property name='family'>microcontroller board (atmega328)</property>
  <property name='variant'>rev 0.1</property>
 </properties>
 <description>Hardkernel ODROID-SHOW2: ATmega328P at 16 MHz and 3.45 V with a 2.2 in 320x240 TFT (Tianma TM022HDH26, ILI9340C), CP2104 USB serial, LiPo charger (XC6802, 4.2 V) and battery connector, power switch, three buttons (PD7, PC0, PC1) and three LEDs (PD3, PD4, PD6). Connectors: the 6-pin I/O header P2 (P3V45, SCL/A5, SDA/A4, ADC3/A3, INT0/D2, GND), the ISP header J1, the DTR reset jumper P1 and the battery connector. Measured from Hardkernel's dimensioned board render; pins from the rev 0.1 schematic.</description>
 <views>
  <iconView><layers image='icon/{stem}_breadboard.svg'><layer layerId='icon'/></layers></iconView>
  <breadboardView><layers image='breadboard/{stem}_breadboard.svg'><layer layerId='breadboard'/></layers></breadboardView>
  <schematicView><layers image='schematic/{stem}_schematic.svg'><layer layerId='schematic'/></layers></schematicView>
  <pcbView><layers image='pcb/{stem}_pcb.svg'><layer layerId='copper0'/><layer layerId='silkscreen'/><layer layerId='copper1'/></layers></pcbView>
 </views>
 <connectors>
{chr(10).join(cons)}
 </connectors>
</module>
"""

stem = 'odroid_show2'
open(OUT + f'part.{stem}.fzp', 'w').write(fzp(stem))
bb = breadboard()
open(OUT + f'svg.breadboard.{stem}_breadboard.svg', 'w').write(bb)
open(OUT + f'svg.icon.{stem}_breadboard.svg', 'w').write(bb.replace("<g id='breadboard'>", "<g id='icon'>"))
open(OUT + f'svg.schematic.{stem}_schematic.svg', 'w').write(schematic())
open(OUT + f'svg.pcb.{stem}_pcb.svg', 'w').write(pcb())
print('ok', len(CON), 'connectors')
