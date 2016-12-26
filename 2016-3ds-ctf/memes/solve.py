from PIL import Image 

def get_pixel(t, x1, y1, img_pix):
    if t == 0:
        r, g, b = img_pix.getpixel((x1, y1))
    elif t == 1: 
        r, b, g = img_pix.getpixel((x1, y1))
    elif t == 2:
        g, r, b = img_pix.getpixel((x1, y1))
    elif t == 3: 
        g, b, r = img_pix.getpixel((x1, y1))
    elif t == 4:       
        b, r, g = img_pix.getpixel((x1, y1))
    elif t == 5: 
        b, g, r = img_pix.getpixel((x1, y1))
        
    return (r, g, b)

def get_flag(flag_len, p, offset, x, y, img_pix):
    flag = ''
    for i in range(flag_len + 1):
        x1 = x + offset
        y1 = y + offset
        r, g, b = get_pixel(p, x1, y1, img_pix)
        if r < 32 or r > 125:
            if flag[:4] == '3DS{': 
                print p, offset, flag
            break
        flag += chr(r)
        x = g
        y = b
    
def parse_file():
    flag = ''
    with Image.open('output.png') as img:
        img_pix = img.convert('RGB')
        height, width = img_pix.size
        flag_len, x, y = get_pixel(0, 0, 0, img_pix)
        for p in range(6):
            for offset in range(height - 255 + 1):
                flag = get_flag(flag_len, p, offset, x, y, img_pix)
      
parse_file()

