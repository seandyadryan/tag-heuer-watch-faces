"""Reject the Wear OS boot overlay: our default papaya dial must be visible."""
import sys
from PIL import Image

image = Image.open(sys.argv[1]).convert('RGB')
orange = sum(1 for r, g, b in image.getdata() if r > 180 and 60 < g < 180 and b < 75)
print(f'Visible papaya pixels: {orange}')
sys.exit(0 if orange > 100 else 1)
