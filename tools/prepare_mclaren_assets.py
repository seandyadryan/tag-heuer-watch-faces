"""Export reference-generated art and compose clock layers without modifying the master.
Requires Pillow. The watch's live hands and date are separate from the background.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
dial = Image.open(ROOT / 'assets/source/mclaren_red_background.png').convert('RGBA').resize((450,450), Image.Resampling.LANCZOS)
def save(image, name):
    for module in ('wear', 'companion'):
        image.save(ROOT / module / 'src/main/res/drawable-nodpi' / f'{name}.png', optimize=True)
save(dial, 'dial_mclaren_red')
sub = Image.new('RGBA', (6,45))
d = ImageDraw.Draw(sub)
d.polygon([(3,0),(5,4),(4,40),(3,44),(1,40),(1,4)], fill='#E5E7E9')
d.line([(3,4),(3,37)], fill='white', width=1)
save(sub, 'subdial_hand')
cap = Image.new('RGBA', (16,16))
d = ImageDraw.Draw(cap)
d.ellipse((1,1,14,14), fill='#5A5B5D', outline='#F1F2F3', width=2)
d.ellipse((5,5,10,10), fill='#C9CDD0')
save(cap, 'metal_cap')
preview = dial.copy()
drawable = ROOT / 'wear/src/main/res/drawable-nodpi'
def hand(name, angle, x, y, cx, cy, tint=None):
    bitmap = Image.open(drawable / f'{name}.png').convert('RGBA')
    if tint:
        colored = Image.new('RGBA', bitmap.size, tint)
        colored.putalpha(bitmap.getchannel('A')); bitmap = colored
    layer = Image.new('RGBA', preview.size)
    layer.alpha_composite(bitmap, (x,y))
    preview.alpha_composite(layer.rotate(-angle, resample=Image.Resampling.BICUBIC, center=(cx,cy)))
hand('subdial_hand',240,143,162,146,202)
hand('subdial_hand',60,291,162,294,202)
hand('subdial_hand',305,217,254,220,294)
for x,y in ((146,202),(294,202),(220,294)):
    preview.alpha_composite(cap.resize((8,8),Image.Resampling.LANCZOS),(x-4,y-4))
hand('hour',305,214,110,225,225)
hand('minute',60,218,56,225,225)
hand('second',240,222,37,225,225,'#BE2837')
preview.alpha_composite(cap,(217,217))
date = Image.new('RGBA',(32,24))
font = Path('C:/Windows/Fonts/arial.ttf')
if not font.exists(): font = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
ImageDraw.Draw(date).text((16,12),'12',fill='white',font=ImageFont.truetype(str(font),15),anchor='mm')
date = date.rotate(-30,resample=Image.Resampling.BICUBIC,expand=True)
preview.alpha_composite(date,(327-date.width//2,278-date.height//2))
save(preview,'preview_mclaren_red')
print('Exported red dial, subdial hand, metal hub and composed preview for both modules.')
