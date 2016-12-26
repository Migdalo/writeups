#!/usr/bin/python

from PIL import Image
import random

FLAG = '3DS{d0_n0t_trY_Th4t}'

def put_pixel(t, x1, y1, r, g, b):
    if t == 0:
        img_pix.putpixel((x1, y1),(r, g, b))
    elif t == 1: 
        img_pix.putpixel((x1, y1),(r, b, g))
    elif t == 2:
        img_pix.putpixel((x1, y1),(g, r, b))
    elif t == 3: 
        img_pix.putpixel((x1, y1),(g, b, r))
    elif t == 4:       
        img_pix.putpixel((x1, y1),(b, r, g))
    elif t == 5: 
        img_pix.putpixel((x1, y1),(b, g, r))

img = Image.open('input.png')
img_pix = img.convert('RGB')

h, w = img_pix.size
x = random.randint(1, 255)
y = random.randint(1, 255)
p = random.randint(1, 255) % 6
offset = random.randint(1, h - 255)

put_pixel(0, 0, 0, len(FLAG), x, y)

for l in FLAG:
    x1 = random.randint(1,255)
    y1 = random.randint(1,255)
    put_pixel(p, x + offset, y + offset, ord(l), x1, y1)
    x = x1
    y = y1

img_pix.save('output.png')
