# Memes
Stego 
300

> Playing another CTFs, our team discovered an awesome algorithm to hid messages in a PNG file.<br>
One member of the team told that is possible to improve the algorithm to make it impossible to retrieve the original message directly. So he hiden a message on this meme and gave to us to solve.<br>
Prove the he's wrong!

We were given a png file and a python script ([weakool.py](./weakool.py)). Reading the script revealed that the other CTF mentioned in the task description was probably HackIt 2016, cause I could remember a couple of tasks from there that were similar to this one. The idea basically is to color a pixel using a decimal presentation of a character from the flag and the coordinates of the next pixel you want to color as RGB values. The script in this task differs from HackIts scripts in its use of random numbers.

To decrypt the flag we need to read the pixels in the correct order. The starting pixel is known, but offset and the order of r, g and b in the pixel colors are not. However, there aren't that many options so they can be brute-forced.

``` python
def parse_file():
    flag = ''
    with Image.open('output.png') as img:
        img_pix = img.convert('RGB')
        height, width = img_pix.size
        flag_len, x, y = get_pixel(0, 0, 0, img_pix)
        for p in range(6):
            for offset in range(height - 255 + 1):
                flag = get_flag(flag_len, p, offset, x, y, img_pix)
```
Inverting the weakool script was pretty straight forward. I replaced the put_pixel function with a get_pixel function that returns the r, g, b values, instead of passing them on. The full script can be found at [solve.py](./solve.py).

``` python
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
```
The correct offset was 2366 and p value 2 (g, r, b). The flag was 3DS{w0w_aw3s0me_scr1pt}.
