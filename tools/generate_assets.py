"""Generate original geometric dial artwork; no third-party logos or photographs.
Requires Pillow. Pass --font to regenerate with a specific TTF on another OS.
"""
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font', default='C:/Windows/Fonts/arial.ttf')
args = parser.parse_args()
SCALE = 3
def font(size):
    return ImageFont.truetype(args.font, size * SCALE)
def text(draw, xy, value, size, fill):
    draw.text(tuple(v * SCALE for v in xy), value, font=font(size), fill=fill, anchor='mm')
def circle(draw, bounds, fill=None, outline=None, width=1):
    draw.ellipse(tuple(v * SCALE for v in bounds), fill=fill, outline=outline, width=width * SCALE)
def line(draw, points, fill, width=1):
    draw.line([(x * SCALE, y * SCALE) for x, y in points], fill=fill, width=width * SCALE)
def point(radius, angle):
    rad = math.radians(angle - 90)
    return 225 + radius * math.cos(rad), 225 + radius * math.sin(rad)
def save(im, name, both=True):
    im = im.resize((im.width // SCALE, im.height // SCALE), Image.Resampling.LANCZOS)
    for module in (['wear', 'companion'] if both else ['wear']):
        path = ROOT / module / 'src/main/res/drawable-nodpi' / (name + '.png')
        path.parent.mkdir(parents=True, exist_ok=True)
        im.save(path, optimize=True)
    return im

im = Image.new('RGBA', (450 * SCALE, 450 * SCALE), 'black')
d = ImageDraw.Draw(im)
circle(d, (6, 6, 444, 444), '#11151B', '#5D626A', 3)
circle(d, (22, 22, 428, 428), '#07090D', '#343940', 1)
circle(d, (49, 49, 401, 401), '#12161C', '#686D75', 1)
circle(d, (57, 57, 393, 393), '#101319', '#232B36', 1)
# Tachymeter-inspired scale, decorative rather than a measurement claim.
for i, value in enumerate(['60','65','70','80','90','100','120','140','160','180','240','300']):
    text(d, point(194, i * 30), value, 12, '#9EA6B2')
for i in range(60):
    major = i % 5 == 0
    line(d, [point(156 if major else 164, i * 6), point(173, i * 6)], '#E4E7EB' if major else '#6D747F', 5 if major else 1)
text(d, (225, 110), 'TAG HEUER', 18, '#F2F3F5')
text(d, (225, 134), 'FORMULA 1', 10, '#A4ACB8')
text(d, (225, 154), 'McLaren', 15, '#F2F3F5')
text(d, (225, 278), '30TH ANNIVERSARY', 10, '#A4ACB8')
text(d, (225, 348), '1985 / 2015', 9, '#8E97A4')
# Deliberately no fake chronograph counters: this is an analog timepiece.
accent = Image.new('RGBA', im.size)
a = ImageDraw.Draw(accent)
a.arc((51 * SCALE, 51 * SCALE, 399 * SCALE, 399 * SCALE), 210, 330, fill='white', width=3 * SCALE)
for angle in (0, 90, 180, 270):
    line(a, [point(156, angle), point(173, angle)], 'white', 3)
circle(a, (218, 218, 232, 232), 'white')
save(im, 'dial')
save(accent, 'accent')
hands = {}
for name, width, height, pivot, tip in [('hour',22,135,115,12), ('minute',14,190,169,8), ('second',6,215,188,3)]:
    hand = Image.new('RGBA', (width * SCALE, height * SCALE))
    hd = ImageDraw.Draw(hand)
    points = [(width/2,0),(width-2,tip),(width-3,pivot),(width/2,height),(3,pivot),(2,tip)]
    hd.polygon([(x*SCALE,y*SCALE) for x,y in points], fill='#EEF1F4' if name != 'second' else 'white')
    if name != 'second':
        line(hd, [(width/2, tip+5),(width/2,pivot-14)], '#76808D', 2)
    hands[name] = save(hand, name)

preview = im.copy()
colored = Image.new('RGBA', im.size, '#FF8700')
colored.putalpha(accent.getchannel('A'))
preview.alpha_composite(colored)
def add_hand(name, angle, x, y):
    layer = Image.new('RGBA', im.size)
    src = hands[name].resize((hands[name].width*SCALE,hands[name].height*SCALE), Image.Resampling.LANCZOS)
    if name == 'second':
        tinted = Image.new('RGBA', src.size, '#FF8700'); tinted.putalpha(src.getchannel('A')); src = tinted
    layer.alpha_composite(src,(x*SCALE,y*SCALE))
    preview.alpha_composite(layer.rotate(-angle, resample=Image.Resampling.BICUBIC, center=(225*SCALE,225*SCALE)))
add_hand('hour',305,214,110)
add_hand('minute',60,218,56)
add_hand('second',240,222,37)
p = ImageDraw.Draw(preview)
circle(p, (218,218,232,232), '#FF8700')
text(p, (225,310),'10:10',26,'#F1F3F5')
save(preview, 'preview')
print('Generated dial, accent, three hands and preview for both modules.')
