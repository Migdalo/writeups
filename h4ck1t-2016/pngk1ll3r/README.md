# Pngk1LL3r - Iran
**Misk 250pts**

>The order from the central management has arrived, but.. We can't open it. And if we don't make it, then we don't get the info about further plans of the command team. But only not in your shift! Fix the file and get the deserved promotion.

The file we got with the task is a png file. However, it can't be opened.

About [PNG](https://www.w3.org/TR/PNG/) files:
* The signature of PNG file is *89 50 4e 47 0d 0a 1a 0a*
* PNG file consists of multiple chunks, some of which are compulsory and others that are optional
* Each PNG chunk consists of fields: length (4 bytes), chunk type (4 bytes), chunk data (the length field shows how many bytes this one has) and CRC (4 bytes)
* The 32-bit CRC is calculated from the preceeding bytes of the chunk, excluding the length field.

I used the following steps to solve this challenge:

1. I started by opening the png file in a hex editor, and noticing that the file signature was wrong. The first byte was *90* and not *89*. I corrected it, but the file could still not be opened. 

2. Next, I ran the file throught [pngcheck](http://www.libpng.org/pub/png/apps/pngcheck.html). It told me that some of the chunks had CRC errors in them. From the output I could also see that '1337' was very common number in different size fields. This could not be a coincidence. I theorised that the CRC's are correct, but chunk length fields had been changed. This would lead to CRC being read from a wrong position, and would explain the erroneous CRC's. 
  ![1337](https://github.com/Migdalo/writeups/blob/master/h4ck1t-2016/pngk1ll3r/pngcheck.png?raw=true)

  I went back to hex editor to search for the expected CRC and found it from a wrong position. This proved my assumption correct. I then proceeded to edit the file to correct the wrong length values.
  1. The iTXt field didn't include anything useful so instead of fixing the chunk length, I deleted the chunk.
  2. Doing a string search looking for IDAT chunk revealed that the file has three IDAT chunks. Their chunk lengths were 01, 21 and 07 (1, 33 and 7 in decimals). Because there was that '1337' again, I knew that I was on the right track, and all of the IDAT chunks most likely had a wrong chunk length. 
    * IDAT strings were located at positions 0x00000076 (= 118), 0x00004082 (= 16514) and 0x0000808e (= 32910). To know the correct length of the third IDAT chunk I also needed to know the position of IEND string. I found it with a string search at 0x0000880d (= 34829).
    * To get the correct chunk data length, I counted the distance between subsequent chunks. This was easily done by counting the distance between the above positions and substracting 12 bytes from the result (length field (4 bytes), chunk type field (4 bytes) and CRC field (4 bytes) are not counted to chunk length). The correct lengths are:
      * IDAT 1: 16514 - 118 - 12 = 16384, converted to hex: 4000
      * IDAT 2: 32910 - 16514 - 12 = 16384, converted to hex: 4000
      * IDAT 3: 34829 - 32910 - 12 = 1907, converted to hex: 773
      
    I then corrected the data chunk lengths of the first and second IDAT chunk to 4000 and the data chunk length of the third IDAT chunk to 773.

3. The only CRC error left at this point was in IHDR chunk. By looking at pngcheck output I could see that the size of the image itself was set to 13x37. There was that '1337' again. Pngcheck told me that the expected CRC of IHDR field was 441f81d8. I assumed that the CRC is correct. Therefore, the correct width and length of the image would be those that produce the expected CRC. I used a short brute-force script to find the correct image size: 551 x 196. After correcting the width and height, I was able to open the file and get the flag.

  ![h4ck1t{st4rb0und_r3c0v3ry_m1$$ion}](https://github.com/Migdalo/writeups/blob/master/h4ck1t-2016/pngk1ll3r/task.png)
