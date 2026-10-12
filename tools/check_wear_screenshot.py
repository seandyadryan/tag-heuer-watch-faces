"""Reject the Wear OS boot overlay: the red McLaren bezel must be visible."""
import sys
from PIL import Image

image = Image.open(sys.argv[1]).convert('RGB')
red = sum(1 for r, g, b in image.getdata() if r > 90 and r > 1.5 * g and r > 1.4 * b)
print(f'Visible red bezel pixels: {red}')
sys.exit(0 if red > 1000 else 1)
