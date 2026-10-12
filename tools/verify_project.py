"""Dependency-free release contracts; runs locally and on GitHub Actions."""
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ANDROID = '{http://schemas.android.com/apk/res/android}'

def strings(path):
    return {e.attrib['name'] for e in ET.parse(path).getroot().findall('string') if e.attrib.get('translatable') != 'false'}

for path in ROOT.glob('*/src/main/**/*.xml'):
    ET.parse(path)
manifest = ET.parse(ROOT / 'wear/src/main/AndroidManifest.xml').getroot()
assert manifest.find('application').attrib[ANDROID + 'hasCode'] == 'false'
assert not list((ROOT / 'wear/src/main').glob('**/*.kt'))
assert not list((ROOT / 'wear/src/main').glob('**/*.java'))
assert not manifest.findall('uses-permission')
face = ET.parse(ROOT / 'wear/src/main/res/raw/watchface.xml').getroot()
colors = face.find('UserConfigurations/ColorConfiguration')
assert colors.attrib['defaultValue'] in {e.attrib['id'] for e in colors}
hand_tags = {'HourHand', 'MinuteHand', 'SecondHand'}
hands = []
for clock in face.findall('.//AnalogClock'):
    for hand in clock:
        if hand.tag not in hand_tags:
            continue
        hands.append(hand)
        pivot_x = float(hand.attrib['x']) + float(hand.attrib['width']) * float(hand.attrib['pivotX'])
        pivot_y = float(hand.attrib['y']) + float(hand.attrib['height']) * float(hand.attrib['pivotY'])
        assert abs(pivot_x - float(clock.attrib['width']) / 2) < .001 and abs(pivot_y - float(clock.attrib['height']) / 2) < .001, hand.tag
for image in face.findall('.//Image') + hands:
    assert (ROOT / 'wear/src/main/res/drawable-nodpi' / (image.attrib['resource'] + '.png')).exists()
main_clock = next(c for c in face.findall('Scene/AnalogClock') if c.attrib['width'] == '450')
assert main_clock.find('SecondHand/Variant').attrib['value'] == '0'
base = strings(ROOT / 'companion/src/main/res/values/strings.xml')
translations = list(ROOT.glob('companion/src/main/res/values-*/strings.xml'))
for path in translations:
    assert strings(path) == base, f'Incomplete translation: {path}'
locales = ET.parse(ROOT / 'companion/src/main/res/xml/locales_config.xml').getroot()
assert len(locales) == len(translations) + 1
total_bytes = 0
for path in ROOT.glob('wear/src/main/res/drawable-nodpi/*.png'):
    data = path.read_bytes()
    width, height = struct.unpack('>II', data[16:24])
    total_bytes += width * height * 4
assert total_bytes < 10 * 1024 * 1024, 'Decoded artwork exceeds ambient budget; run official evaluator'
for apk in ROOT.glob('wear/build/outputs/apk/**/*.apk'):
    with zipfile.ZipFile(apk) as bundle:
        assert not any(n.endswith('.dex') for n in bundle.namelist()), 'WFF APK must not contain code'
print(f'PASS: WFF resource contracts, hand pivots, {len(locales)} full locales, no executable wear code.')
print(f'Decoded artwork upper bound: {total_bytes / 1048576:.2f} MiB; official evaluator runs in CI.')
