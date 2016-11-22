# Breaking News

> Breaking News

> 300

> We just received this transmission from our news correspondents. We need to find out what they are telling us.

> Download Link: https://drive.google.com/file/d/0B_AQp5s_S-khWjExSllLYjFRR0E/view?usp=sharing

We were given 20 zip archives. I opened one of them to see what was inside, and discovered that the only content was a single text file. The file didn't have much in it:

```
Coming to you live from QuarfBlaaaark 7, this is Montgomery Flaaaargendach with Live Forensic Files:  
Raw Forensic Adventures.
```

I wrote a Python script to find out what was inside the rest of the archives.

``` python
import os, zipfile

directory = os.getcwd() + '/Forensics-300' + '/'

for filename in os.listdir(directory):
    fn = filename.split('.')
    if fn[1] == 'zip':
        z = zipfile.ZipFile(directory + filename)
        print z.namelist()
```

The script showed that each of the archives only had one text file in each of them. I then turned to the only other files available, which were the zip archives themselves. I opened a few of them in a hex editor. At the end of Chapter4.zip, I found a piece of text that looked like base64. It turned out to be base64 encoding of 'RC' (UkMK), which is the start of the flag.

![Hex-editor](https://github.com/Migdalo/writeups/blob/master/rc3-ctf-2016/breaking_news/zip_file_hex_editor.png)

From the [zip file specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT) we can learn that the end of zip file field starts with bytes 0x06054g50 and is 22 bytes long. Also, all values are stored in little-endian byte order unless otherwise stated.

I wrote a Python script that looks for the end of zip directory central record and prints out any data that appears after it.

``` python
for filename in sorted(os.listdir(directory), cmp=lambda x, y: cmp(get_num(x), get_num(y))):
    with open(directory + filename, 'rb') as f:
        content = f.read()
        hexed = binascii.hexlify(content)
        for i in range(len(hexed)):
            if zipend == hexed[i:i+8]:
                found = hexed[i + 22 * 2:]
                if found:
                    #flag.append(b64d(found.decode('hex')).strip())
                    print found.decode('hex')
```

With this script I was able to find five strings that appeared after the end of the zip archive.
```
QkxTCg==
S1lGCg==
MTYtRFUK
UkMK
My0yMAo=
```
I then decoded each of the base64 strings individually and appended them together to get the flag:
```
RC3-2016-DUKYFBLS
```
