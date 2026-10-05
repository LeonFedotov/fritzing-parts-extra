# Generates the RedBear BLE Nano v1.5 Fritzing part from RedBear's v1.5
# gerbers (pad positions), in a checkout of github.com/redbear/nRF5x:
#
#   python3 -m venv .venv && .venv/bin/pip install gerbonara
#   .venv/bin/python tools/redbear_ble_nano_v1_5.py ~/code/nRF5x
#
# The outline (18.5 x 20.887 mm) and the gerber-to-board offsets come from
# RedBear's DXF (nRF51822/docs/nRF51822 Nano V1.5.dxf).
import os
import sys
import tempfile
import warnings
import zipfile
warnings.filterwarnings('ignore')
from gerbonara import GerberFile
from gerbonara.graphic_objects import Flash

if len(sys.argv) != 2:
    sys.exit('usage: redbear_ble_nano_v1_5.py <redbear/nRF5x checkout>')
_tmp = tempfile.mkdtemp()
zipfile.ZipFile(os.path.join(sys.argv[1], 'nRF51822/pcb/BLE Nano v1.5 gerber.zip')).extractall(_tmp)
D = os.path.join(_tmp, 'BLE Nano v1.5 geber') + '/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'redbear-ble-nano-v1.5') + '/'
os.makedirs(OUT, exist_ok=True)
W, H = 18.5, 20.887  # board, mm (DXF outline)

def loc(x, y):  # gerber inch -> board mm, top view, y down
    return x * 25.4 - 508 + 9.25, 30.037 - (y * 25.4 - 386.807)

def flashes(layer, num):
    return [loc(o.x, o.y) for o in GerberFile.open(D + layer + '.pho').objects
            if isinstance(o, Flash) and o.aperture.original_number == num]

tht = sorted(flashes('art001', 18))            # 12 header pads, 1.8 mm
edge = sorted(flashes('art004', 88))           # 5 bottom-side pads, 1.2 x 2.0 mm
mod_side = flashes('art001', 82)               # module pads, 1.8 x 0.45 mm
mod_bottom = flashes('art001', 83)             # module pads, 0.45 x 1.8 mm

left = sorted([p for p in tht if p[0] < W / 2], key=lambda p: p[1])
right = sorted([p for p in tht if p[0] > W / 2], key=lambda p: p[1])
edge = sorted(edge, key=lambda p: p[0])

# Top view (module up). Names, then what the pin is for.
PINS = (
    [(p, n, d) for p, (n, d) in zip(left, [
        ('VDD', '3.3 V rail: output when powered from VIN, or supply in (1.8 to 3.6 V)'),
        ('P0_10', 'D2, UART CTS, SPI CS, I2C SDA'),
        ('P0_9', 'D1, UART TXD, SPI MOSI'),
        ('P0_11', 'D0, UART RXD, SPI MISO'),
        ('P0_8', 'D3, UART RTS, SPI SCK, I2C SCL'),
        ('GND', 'ground')])]
    + [(p, n, d) for p, (n, d) in zip(right, [
        ('SWCLK', 'SWD clock'),
        ('SWDIO', 'SWD data'),
        ('P0_4', 'A3, analog in'),
        ('P0_5', 'A4, analog in'),
        ('GND', 'ground'),
        ('VIN', 'supply in, 3.3 to 13 V, through the on-board regulator')])]
    + [(p, n, d) for p, (n, d) in zip(edge, [
        ('P0_28', 'D4, pad on the underside'),
        ('P0_29', 'D5, pad on the underside'),
        ('P0_15', 'D6, pad on the underside'),
        ('P0_6', 'A5, analog in, pad on the underside'),
        ('P0_7', 'D7, pad on the underside')])])
SILK = {'VDD': 'VDD', 'P0_10': 'CTS', 'P0_9': 'TXD', 'P0_11': 'RXD', 'P0_8': 'RTS', 'SWCLK': 'CLK', 'SWDIO': 'DIO',
        'P0_4': 'P04', 'P0_5': 'P05', 'GND': 'GND', 'VIN': 'VIN', 'P0_28': 'P28', 'P0_29': 'P29', 'P0_15': 'P15',
        'P0_6': 'P06', 'P0_7': 'P07'}
GOLD, RING_DARK, PCB, SILK_C = '#d6b052', '#9c7a2a', '#cf3b2b', '#ffffff'
FONT = "font-family='OCRA, Droid Sans Mono, monospace'"

def f(v): return f'{v:.3f}'

def breadboard():
    s = [f"<?xml version='1.0' encoding='UTF-8'?>",
         "<!-- RedBear BLE Nano v1.5, top (module) side. Pads, holes and outline from RedBear's v1.5 gerbers and DXF;",
         "     pin labels are the bottom silkscreen's, shown on top for reading. -->",
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{W / 25.4:.5f}in' height='{H / 25.4:.5f}in' viewBox='0 0 {W} {H}'>",
         "<g id='breadboard'>",
         f"<rect x='0' y='0' width='{W}' height='{H}' rx='1.5' fill='{PCB}' stroke='#a32a1e' stroke-width='0.12'/>"]
    # underside pads at the bottom edge, drawn first: the module overlaps them
    for (x, y), name, _ in PINS[12:]:
        s.append(f"<rect x='{f(x - 0.6)}' y='{f(y - 1.0)}' width='1.2' height='2' fill='{GOLD}' stroke='{RING_DARK}' stroke-width='0.08'/>")
    # module: PCB, castellated pads, antenna, shield can
    s.append(f"<rect x='4.15' y='0.58' width='10.2' height='{f(17.0 - 0.58)}' rx='0.3' fill='#2d4f6e' stroke='#1d364c' stroke-width='0.08'/>")
    for x, y in mod_side:
        s.append(f"<rect x='{f(x - 0.4)}' y='{f(y - 0.17)}' width='0.8' height='0.34' fill='{GOLD}'/>")
    for x, y in mod_bottom:
        s.append(f"<rect x='{f(x - 0.17)}' y='{f(y - 0.4)}' width='0.34' height='0.8' fill='{GOLD}'/>")
    ant = 'M5.2,3.0 V1.3 H6.2 V2.6 H7.2 V1.3 H8.2 V2.6 H9.2 V1.3 H10.2 V2.6 H11.2 V1.3 H12.2 V2.6 H13.3'
    s.append(f"<path d='{ant}' fill='none' stroke='{GOLD}' stroke-width='0.3' stroke-linejoin='round'/>")
    s.append("<rect x='5.0' y='3.5' width='8.5' height='12.6' rx='0.35' fill='#cfd3d8' stroke='#8e949b' stroke-width='0.12'/>")
    s.append("<rect x='5.45' y='3.95' width='7.6' height='11.7' rx='0.25' fill='none' stroke='#b4b9bf' stroke-width='0.08'/>")
    s.append(f"<text x='9.25' y='9.4' {FONT} font-size='0.95' fill='#6d737a' text-anchor='middle'>nRF51822</text>")
    s.append(f"<text x='9.25' y='10.7' {FONT} font-size='0.75' fill='#6d737a' text-anchor='middle'>BLE Nano</text>")
    # silkscreen: bear, GND / VIN, pin labels
    s.append(f"<g fill='{SILK_C}'><circle cx='16.45' cy='1.85' r='1.05'/><circle cx='15.55' cy='0.95' r='0.33'/><circle cx='17.35' cy='0.95' r='0.33'/></g>")
    s.append(f"<ellipse cx='16.45' cy='2.2' rx='0.32' ry='0.2' fill='{PCB}'/>")
    s.append(f"<text x='0.9' y='20.3' {FONT} font-size='0.9' fill='{SILK_C}'>GND</text>")
    s.append(f"<text x='17.6' y='20.3' {FONT} font-size='0.9' fill='{SILK_C}' text-anchor='end'>VIN</text>")
    for i, ((x, y), name, _) in enumerate(PINS):
        label = SILK[name]
        if i < 12:  # beside the pin, toward the module, read bottom to top
            tx = x + (1.45 if x < W / 2 else -1.05)
            s.append(f"<text transform='translate({f(tx)},{f(y)}) rotate(-90)' {FONT} font-size='0.72' fill='{SILK_C}' text-anchor='middle'>{label}</text>")
        else:
            s.append(f"<text x='{f(x)}' y='19.25' {FONT} font-size='0.62' fill='{SILK_C}' text-anchor='middle'>{label}</text>")
    # header pins, the connectors
    for i, ((x, y), name, _) in enumerate(PINS[:12]):
        s.append(f"<circle id='connector{i}pin' cx='{f(x)}' cy='{f(y)}' r='0.9' fill='{GOLD}' stroke='{RING_DARK}' stroke-width='0.1'/>")
        s.append(f"<rect x='{f(x - 0.32)}' y='{f(y - 0.32)}' width='0.64' height='0.64' fill='#8c8c8c'/>")
    for i, ((x, y), name, _) in enumerate(PINS[12:], start=12):
        s.append(f"<rect id='connector{i}pin' x='{f(x - 0.6)}' y='{f(y + 0.55)}' width='1.2' height='0.45' fill='none'/>")
    s += ["</g>", "</svg>", ""]
    return '\n'.join(s)

def schematic():
    # A box with 0.1 in pins: power and debug left, I/O right (Fritzing's schematic grid).
    lp = ['VIN', 'VDD', 'GND', 'GND', 'SWDIO', 'SWCLK']
    rp = ['P0_11', 'P0_9', 'P0_10', 'P0_8', 'P0_28', 'P0_29', 'P0_15', 'P0_7', 'P0_4', 'P0_5', 'P0_6']
    pitch, pin_len, w = 0.1, 0.1, 0.8
    h = pitch * (max(len(lp), len(rp)) + 1)
    ids = {}
    for i, (_, name, _) in enumerate(PINS):
        ids.setdefault(name, []).append(i)
    used = {k: 0 for k in ids}
    def cid(name):
        i = ids[name][used[name]]; used[name] += 1; return i
    s = [f"<?xml version='1.0' encoding='UTF-8'?>",
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{w + 2 * pin_len:.3f}in' height='{h:.3f}in' viewBox='0 0 {(w + 2 * pin_len) * 100:.1f} {h * 100:.1f}'>",
         "<g id='schematic'>",
         f"<rect x='{pin_len * 100}' y='0' width='{w * 100}' height='{h * 100}' fill='none' stroke='#000' stroke-width='1'/>",
         f"<text x='{(pin_len + w / 2) * 100}' y='7' font-family='Droid Sans' font-size='7' text-anchor='middle'>BLE Nano v1.5</text>"]
    for side, pins in (('l', lp), ('r', rp)):
        for k, name in enumerate(pins):
            y = (k + 1) * pitch * 100
            i = cid(name)
            x0 = 0 if side == 'l' else (pin_len + w) * 100
            s.append(f"<line id='connector{i}pin' x1='{x0}' y1='{y}' x2='{x0 + pin_len * 100}' y2='{y}' stroke='#000' stroke-width='1'/>")
            tx = x0 + 1 if side == 'l' else x0 + pin_len * 100 - 1
            s.append(f"<rect id='connector{i}terminal' x='{tx - 1 if side == 'l' else tx}' y='{y - 0.5}' width='1' height='1' fill='none'/>")
            lx = (pin_len * 100 + 2) if side == 'l' else ((pin_len + w) * 100 - 2)
            s.append(f"<text x='{lx}' y='{y + 2.5}' font-family='Droid Sans' font-size='7' text-anchor='{'start' if side == 'l' else 'end'}'>{name}</text>")
    s += ["</g>", "</svg>", ""]
    return '\n'.join(s)

def pcb():
    s = [f"<?xml version='1.0' encoding='UTF-8'?>",
         f"<svg xmlns='http://www.w3.org/2000/svg' width='{W / 25.4:.5f}in' height='{H / 25.4:.5f}in' viewBox='0 0 {W} {H}'>",
         f"<g id='silkscreen'><rect x='0.05' y='0.05' width='{W - 0.1}' height='{H - 0.1}' rx='1.45' fill='none' stroke='#000' stroke-width='0.1'/></g>"]
    for layer in ('copper0', 'copper1'):
        s.append(f"<g id='{layer}'>")
        for i, ((x, y), _, _) in enumerate(PINS[:12]):
            s.append(f"<circle id='connector{i}pad' cx='{f(x)}' cy='{f(y)}' r='0.675' fill='none' stroke='#F7BD13' stroke-width='0.45'/>")
        if layer == 'copper0':
            for i, ((x, y), _, _) in enumerate(PINS[12:], start=12):
                s.append(f"<rect id='connector{i}pad' x='{f(x - 0.6)}' y='{f(y - 1.0)}' width='1.2' height='2' fill='#F7BD13'/>")
        s.append("</g>")
    s += ["</svg>", ""]
    return '\n'.join(s)

def fzp(stem):
    cons = []
    for i, (_, name, desc) in enumerate(PINS):
        smd = i >= 12
        pcb_views = (f"<p layer='copper0' svgId='connector{i}pad'/>" if smd else
                     f"<p layer='copper0' svgId='connector{i}pad'/><p layer='copper1' svgId='connector{i}pad'/>")
        cons.append(f"""  <connector id='connector{i}' name='{name}' type='{'pad' if smd else 'male'}'>
   <description>{desc}</description>
   <views>
    <breadboardView><p layer='breadboard' svgId='connector{i}pin'/></breadboardView>
    <schematicView><p layer='schematic' svgId='connector{i}pin' terminalId='connector{i}terminal'/></schematicView>
    <pcbView>{pcb_views}</pcbView>
   </views>
  </connector>""")
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<module fritzingVersion='1.0.0' moduleId='RedBearBLENanoV1_5ModuleID'>
 <version>1</version>
 <title>RedBear BLE Nano v1.5</title>
 <label>U</label>
 <date>2026-10-06</date>
 <author>fritzing-parts-extra, from RedBear's published v1.5 gerbers and pinout</author>
 <tags><tag>RedBear</tag><tag>BLE Nano</tag><tag>nRF51822</tag><tag>Bluetooth Low Energy</tag><tag>BLE</tag></tags>
 <properties>
  <property name='family'>microcontroller board (nRF51822)</property>
  <property name='variant'>v1.5</property>
 </properties>
 <description>RedBear BLE Nano v1.5: Nordic nRF51822 (Cortex-M0, BLE) on an 18.5 x 20.9 mm board. Two rows of six 0.1 in header pins, 0.6 in apart, and five pads on the underside's bottom edge. Arduino pins: D0 P0_11, D1 P0_9, D2 P0_10, D3 P0_8, D4 P0_28, D5 P0_29, D6 P0_15, D7 P0_7, D13 P0_19 (on-board LED), A3 P0_4, A4 P0_5, A5 P0_6. UART pins with the factory jumper settings (S1-S5 shorted). Geometry from RedBear's v1.5 gerbers (github.com/redbear/nRF5x); the breadboard drawing shows the module side, with the underside's pin labels.</description>
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

stem = 'redbear_ble_nano_v1_5'
open(OUT + f'part.{stem}.fzp', 'w').write(fzp(stem))
bb = breadboard()
open(OUT + f'svg.breadboard.{stem}_breadboard.svg', 'w').write(bb)
open(OUT + f'svg.icon.{stem}_breadboard.svg', 'w').write(bb.replace("<g id='breadboard'>", "<g id='icon'>"))
open(OUT + f'svg.schematic.{stem}_schematic.svg', 'w').write(schematic())
open(OUT + f'svg.pcb.{stem}_pcb.svg', 'w').write(pcb())
print('pins', [(n, round(p[0], 2), round(p[1], 2)) for p, n, _ in PINS])
