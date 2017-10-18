# Threat 2

As part of this challenge we were given 56 executable files and following instructions:

```
netcat your answer to 52.42.81.161:8082
Given the included archive of malware samples:

Find the longest, contiguous, most efficient rule to catch all of them.
The rule must use the hexadecimal format. 
The rule CANNOT fire on any other samples. ONLY the 56 provided.
The wildcard ("?" or "??") is allowed but not jumps 
"[1-6]". See http://yara.readthedocs.io/en/latest/writingrules.html#hexadecimal-strings 
The samples are included in yara_samples.7z password is "infected"

The rule must follow this example format:

rule yara_challenge
{
	strings:
		$yara_challenge = { de ad b? ef ?? ??}
	condition:
		 all of them 
}

You will change the contents of $yara_challenge from "de ad b? ef ?? ??" to a 
hex formatted rule that will catch all 56 samples.

Use this template when submitting your rule:

rule yara_challenge
{
	strings:
		$yara_challenge = { ** ** ** ** ** ** }
	condition:
		 all of them 
} 

Hint:
There are 308 wildcard "?"'s within the answer
```

The file sizes varied from 96.3 kB to 693.0 kB, but some of the files were of the same size. I compared some of the files with a same file size against each other in a hex editor and noticed that large parts of those files were the same, or very similiar to each other. I tried converting the files to hex and comparing them to all the other files that had the same file size. I replaced the differing hex characters with question marks. 

``` python
import os
import sys

path = './files/'
tmp_path = './hex/'

def read_files(path):
    filedata = []
    for filename in os.listdir(path):
        with open(path + filename, 'rb') as infile:
            data = infile.read().encode('hex')
        filedata.append((filename, data, len(data)))
    return filedata

def compare_multiple_files(short_files, tmp_path):
    diff = ''
    for filename in short_files:
        with open('./files/' + filename, 'r') as f:
            data = f.read().encode('hex')
        if not diff:
            diff = data
            continue
        tmp = diff
        diff = ''
        count = 0
        for i in range(len(data)):
            try:
                if data[i] == tmp[i]:
                    diff += data[i]
                else:
                    diff += '?'
                    count += 1
            except IndexError:
                break
    with open(tmp_path + short_files[0] + '_diff', 'wb') as outfile:
        outfile.write(diff)
    return diff

def start(tmp_path):
    filedata = read_files(path)
    filelengths = list(set([f[2] for f in filedata]))
    for length in filelengths: # compare files of the same length
        files = [f[0] for f in filedata if f[2] == length]
        compare_multiple_files(files, tmp_path)

if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)
start(tmp_path)
```

This reduced the number of files from 56 down to 24. The highest count of files with the same file size was six. Because the rule cannot fire on any other samples, it was save to ignore long sequences of zeros and question marks.

``` python
def find_index(path, files):
    phrase = '53568b35'
    diff_end = ''
    for filename in files:
        with open(path + filename, 'r') as infile:
            data = infile.read()
        try:
            data.index(phrase)
        except ValueError as ve:
            print(ve)
            return
        if not diff_end:
            diff_end = data[data.index(phrase):]
            continue
        tmp = diff_end
        diff_end = ''
        count = 0
        for i in range(len(tmp)):
            try:
                if data[data.index(phrase) + i] == tmp[i]:
                    diff_end += data[data.index(phrase) + i]
                else:
                    diff_end += '?'
                    count += 1
            except IndexError:
                break
            except ValueError:
                print filename
                break
    count = 0
    diff_end = diff_end.upper()
    for i in range(0, len(diff_end), 2):
        if diff_end[i] == '?':
            count += 1
        if diff_end[i+1] == '?':
            count += 1
        if count > 308:
            break
        print diff_end[i] + diff_end[i+1],

files = os.listdir(tmp_path)
find_index(tmp_path, files)
```

The solution was:
``` yara
rule yara_challenge
{
  strings:
    $yara_challenge = { 53 56 8B 35 ?? ?? ?? ?0 57 68 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 8B F8 FF D6 68
            ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 FF D6 8B 35 ?? ?? ?? ?0 68 ?? ?? ?? ?0 57 8B D8 FF D6 68 
            ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 
            57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? 
            ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 
            68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? 
            ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 53 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 53 A3 ?? 
            ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF 
            D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 A3 ?? ?? ?? ?0 57 FF D6 68 ?? ?? 
            ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 68 ?? ?? ?? ?0 57 A3 ?? ?? ?? ?0 FF D6 5F 5E A3 ?? ?? ?? ?0 
            5B C3 }
  condition:
    all of them 
}
```

The flag was: PAN{AllByMyself}
