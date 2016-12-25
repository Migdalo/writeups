import os, binascii, sys, pytesseract
from StringIO import StringIO
from PIL import Image

def read_text_from_image(content, filecount):
    try:
        print filecount
        img = Image.open(StringIO(content.decode('hex')))
        img_text = pytesseract.image_to_string(img, \
            config='-psm 6') 
        if img_text[:4] == '3DS{':
            with open('flag%d.jpg' % filecount, 'wb') as f:
                f.write(content.decode('hex'))
            print filecount, img_text
    except KeyboardInterrupt as key:
        sys.exit()
    except IOError:
        return

def extract_files():
    filename = os.getcwd() + '/data'
    search_hex = '46494600'
    jfif_signature = 'FFD8FFE000004A'
    filecount = 0
    i = 0
    content = ''
    with open(filename, 'r') as f:
        while True:
            f.seek(i)
            byte = f.read(8)
            if byte == search_hex:
                read_text_from_image(content, filecount)
                content = jfif_signature
                filecount += 1
                i += 8
            else:
                f.seek(i)
                byte = f.read(2)
                if byte:
                    content += byte
                    i += 2
                else:
                    read_text_from_image(content, filecount)
                    return

extract_files()
