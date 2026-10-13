"""Compose store layouts from an AI-edited product cutout and real app captures.

Photo editing is performed by imagegen; this script only typesets, scales, and
places supplied assets. Run with Pillow; pass --font-dir for other platforms.
"""
from pathlib import Path
import argparse
import math
import zipfile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/play-console'
SRC = OUT / 'source'
SHOTS = OUT / 'screenshots'
SHOTS.mkdir(exist_ok=True)
args = argparse.ArgumentParser()
args.add_argument('--font-dir', default='C:/Windows/Fonts')
fonts = Path(args.parse_args().font_dir)
WHITE = '#F6F4F1'
GREY = '#B9BDC5'
RED = '#EC3C4E'

def font(size, bold=False):
    return ImageFont.truetype(str(fonts / ('arialbd.ttf' if bold else 'arial.ttf')), size)

def text(im, xy, value, size=36, color=WHITE, bold=False):
    d = ImageDraw.Draw(im)
    for line in value.split('\n'):
        bounds = d.textbbox(xy, line, font=font(size, bold))
        assert bounds[2] <= im.width - 25, (value, bounds)
        d.text(xy, line, font=font(size, bold), fill=color)
        xy = (xy[0], xy[1] + int(size * 1.2))

def background(w, h):
    im = Image.new('RGB', (w, h))
    # Code-native racing backdrop; no external photography is altered.
    pix = im.load()
    for y in range(h):
        for x in range(w):
            glow = math.exp(-(((x/w-.86)/.6)**2 + ((y/h-.42)/.55)**2)*3)
            pix[x, y] = (int(9+31*glow), int(11+5*glow), int(15+7*glow))
    d = ImageDraw.Draw(im)
    for offset in range(-h, w, 140):
        d.line((offset, h, offset+h, 0), fill='#191B20', width=1)
    d.rectangle((0, 0, w, 8), fill=RED)
    return im

def place(im, source, box, phone=False):
    asset = source.copy() if isinstance(source, Image.Image) else Image.open(source)
    asset.thumbnail((box[2], box[3]), Image.Resampling.LANCZOS)
    x = box[0] + (box[2]-asset.width)//2
    y = box[1] + (box[3]-asset.height)//2
    if phone:
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((x-12,y-12,x+asset.width+12,y+asset.height+12), 38, fill='#080A0D', outline='#444951', width=3)
    im.paste(asset, (x,y), asset.getchannel('A') if asset.mode == 'RGBA' else None)

def panel(number, title, subtitle):
    im = background(1080,1920)
    text(im,(68,65),'FORMULA 1  /  30TH ANNIVERSARY',27,RED,True)
    text(im,(68,134),title,76,WHITE,True)
    text(im,(70,325),subtitle,31,GREY)
    text(im,(68,1836),'WEAR OS 4+',29,WHITE,True)
    text(im,(866,1836),f'{number:02d} / 06',28,GREY)
    return im

def save(im, name):
    im.convert('RGB').save(name, optimize=True)

watch = Image.open(SRC/'watch-mockup.png')
en = Image.open(SRC/'phone-en.png')
idn = Image.open(SRC/'phone-id.png')
arabic = Image.open(SRC/'phone-ar.png')
guide = Image.open(SRC/'phone-guide-id.png')

feature = background(1024,500)
text(feature,(48,53),'FORMULA 1',23,RED,True)
text(feature,(45,110),'TAG Heuer\nMcLaren',63,WHITE,True)
text(feature,(48,277),'30TH ANNIVERSARY',24,RED,True)
text(feature,(48,337),'Racing heritage, on your wrist.',22,GREY)
text(feature,(48,423),'WATCH FACE  /  WEAR OS 4+',19,WHITE,True)
place(feature,watch,(560,15,435,475))
save(feature,OUT/'feature-graphic-1024x500.png')

im = panel(1,'RACING HERITAGE.\nON YOUR WRIST.','Black dial. Red bezel. Silver details.')
place(im,watch,(65,418,785,1340))
place(im,en,(744,1090,255,568),phone=True)
text(im,(713,1693),'APP PREVIEW',23,GREY,True)
save(im,SHOTS/'01-racing-heritage.png')

im = panel(2,'YOUR ANALOG\nEVERYDAY.','Explore the watch face in the phone app.')
place(im,en,(170,416,740,1345),phone=True)
save(im,SHOTS/'02-analog-preview.png')

im = panel(3,'THREE SUBDIALS.\nONE MOMENT.','Seconds, minutes and 12-hour time.')
# A crop of the real phone capture, preserving the rendered hands and date.
face = en.crop((105,630,975,1500))
place(im,face,(60,470,960,960))
text(im,(70,1485),'CURRENT TIME, IN MOTION',37,WHITE,True)
text(im,(70,1560),'A date window follows the device date.\nSubdials display time, not a stopwatch.',32,GREY)
text(im,(70,1718),'ACTUAL APP PREVIEW',24,RED,True)
save(im,SHOTS/'03-subdials-and-date.png')

im = panel(4,'CHOOSE YOUR\nSECOND HAND.','Red, ice blue or silver. The bezel stays red.')
place(im,en.crop((45,610,1035,1810)),(70,432,940,1160),phone=True)
text(im,(72,1640),'MAKE IT YOURS',39,WHITE,True)
text(im,(72,1701),'Set the watch color in Edit / Customize.',30,GREY)
save(im,SHOTS/'04-accent-options.png')

im = panel(5,'FROM PHONE\nTO WRIST.','Pair. Install on the watch. Select the face.')
place(im,guide,(195,416,690,1345),phone=True)
save(im,SHOTS/'05-installation-guide.png')

im = panel(6,'A GUIDE IN\nYOUR LANGUAGE.','21 app languages, with English fallback.')
place(im,idn,(63,575,449,1000),phone=True)
place(im,arabic,(568,575,449,1000),phone=True)
text(im,(143,1630),'INDONESIAN',25,WHITE,True)
text(im,(729,1630),'ARABIC',25,WHITE,True)
text(im,(70,1720),'Preview captures from the Android companion.',30,GREY)
save(im,SHOTS/'06-language-support.png')

# Preview sheet is a review aid, not an upload asset.
sheet = Image.new('RGB',(1080,1320),'#090B0F')
for i,path in enumerate(sorted(SHOTS.glob('*.png'))):
    thumb = Image.open(path).resize((324,576),Image.Resampling.LANCZOS)
    sheet.paste(thumb,(18+(i%3)*360,24+(i//3)*650))
    text(sheet,(18+(i%3)*360,607+(i//3)*650),path.name[:2],23,GREY)
save(sheet,OUT/'screenshots-preview.jpg')

deliverables = [OUT/'feature-graphic-1024x500.png', *sorted(SHOTS.glob('*.png'))]
for path in deliverables:
    with Image.open(path) as im:
        expected = (1024,500) if path == deliverables[0] else (1080,1920)
        assert im.size == expected and im.mode == 'RGB', (path,im.size,im.mode)
with zipfile.ZipFile(OUT/'play-console-graphics.zip','w',zipfile.ZIP_DEFLATED) as z:
    for path in deliverables:
        z.write(path,path.relative_to(OUT))
print('Verified 1 feature graphic and 6 screenshots: exact dimensions, RGB PNG.')
