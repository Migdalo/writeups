#RTFspy - China
**150pts**

> EN: Everybody likes to store passwords in txt files? And our guinea pig has gone much further! He has begun to store the information under a signature stamp "TOP SECRET" in them! Prove to him that it isn't secure.

The file we got as part of the task is an RTF file. 

Below is a screenshot of the cat results. I cut off the middle of the output so, that I could fit both the start and the end of the file to a single screen.

![](https://github.com/Migdalo/writeups/blob/master/h4ck1t-2016/rtfspy/cat3.png?raw=true)

It seemed at first that the file had many lines, but with 'wc -l' command I could see that there were only five. One of them is a long one and looks very much like hex code. The first byte is 00, but from there onward I could read a PNG signature 89 50 4e 47 0d 0a 1a 0a. This led me to assume that the hex code represents a PNG file. My initial thought was to clean the file up with a python script and paste the clean hex code to a hex editor to see what's inside. However, I wanted to see how much of that could be done from the command line. 

Since none of the other lines besides the hex line had anything useful in them, I started by removing those lines and leaving only the hex line. Because the hex line was the only line that contained a characted sequence /', this could be done with grep.

``` 
grep /' test.rtf
```

Next I had to clean the extra punctuation characters (/'). The tr command seemed like a good way to do this.

```
grep /' test.rtf | tr -delete [:punct:]
```

I wanted to see if the PNG image is actually a viewable one, and weather it has the flag prined on it or not. However, due to the initial /'00 in the file, it was not yet possible to convert the hex string to a image. I removed those extra digits with cut command and piped the result to xxd to convert the plain hexdump to binary.

```
grep /' test.rtf | tr -delete [:punct:] | cut -c 3- | xxd -r -p >> task.png
```

This resulted in a picture of Homer Sipmson, but no flag. I theorised that there might be another file hidden inside the PNG file. To find out if my guess was right, I decided to pipe the output of xxd to foremost. At this point the cut command became unnecessary, so I removed it. Leaving it in wouldn't have had any harm thought.

```
grep /' test.rtf | tr -delete [:punct:] | xxd -r -p | foremost
```

Foremost found a zip file, which in turn contained a text file that cointained the flag. 

The flag is: h4ck1t{rtf_d0cs_4r3_awesome}
