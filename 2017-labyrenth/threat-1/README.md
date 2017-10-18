# Threat 1

As part of this challenge we were given a pcap file. I opened it in Wireshark and noticed that it contained some DNS traffic, and that the packets had base64 encoded data in them.

I printed out the packet loads with the following script:

``` python
from __future__ import print_function
from scapy.all import *

def get_dns_load(pcap_filename):
    with PcapReader(pcap_filename) as pcap:
        for p in pcap:
            pkt = p.payload
            try:
                print(pkt.load)
            except AttributeError:
                continue

pcap_filename = 'challenge.pcap'
get_dns_load(pcap_filename)
```
The result was:

> google�;UEsDBBQAAAAIAOCIr0qMVwGeKQAAACoAcom
youtube�<AAAIABwAZmlsZS5kYXRVVAkAA3QYGlmBcom
facebook�=GBpZdXgLAAEE6AMAAAToAwAAC3D0q3bMcom
baidu�:yQnIz8wrSS0q9sxz8QsOzsgvzUkBCzklcom
	wikipedia�>JmeXJxalFNdyAQBQSwECHgMUAAAACADgorg
yahoo�:iK9KjFcBnikAAAAqAAAACAAYAAAAAAABcom
qq�7AAAAtIEAAAAAZmlsZS5kYXRVVAUAA3QYcom
reddit�;Gll1eAsAAQToAwAABOgDAABQSwUGAAAAcom  
google�/AAEAAQBOAAAAawAAAAAAcoin

These looked like encoded domain names. More information about them is available here: [Domain names - Implementation and specification](https://tools.ietf.org/html/rfc1035). The domain names seemed to follow a pattern: number of characters, characters, pointer to the next number of characters, base64 encoded string, number of characters, characters and finally a terminator. The last domain name had a second sequence of number of characters and characters before the terminator.

Finally, I wrote the following code to extract the base64 encoded parts from the packets, append them together and decode the result. The decoded result looked like a zip file so, I saved it to a file.

``` python
import binascii

def parse_dns_domain_name(load):
    s = [x[2:].zfill(8) for x in map(bin, bytearray(load))]
    i = 0
    line = ''
    while True:
        bstr = s[i]
        i += 1
        if bstr == '00000000':
            # Zero is the terminator.
            line += '0'
            break
        elif bstr.startswith('11'):
            # Pointer starts with 11xxxxxx
            # and is 2 octets long.
            pointer = bstr + s[i]
            jump = int(s[i], 2)
            line += str(pointer)
            flag = ''
            i += 1
            jump = jump-18-i
            for k in range(jump):
                flag += binascii.unhexlify('%x' % int(s[i+k], 2))
            i += jump
            line += flag
        elif bstr.startswith('00'):
            # Label starts with 00, and the first octet
            # represents a lenght of the label.
            l1 = int(bstr, 2)
            line += str(l1)
            for k in range(l1):
                line += binascii.unhexlify('%x' % int(s[i+k], 2))
            i += l1
        else:
            print('This should not happen')
    print(line)
    return flag

def iterate_packets(pcap_filename):
    with PcapReader(pcap_filename) as pcap:
        result = ''
        for p in pcap:
            pkt = p.payload
            try:
                result += parse_dns_domain_name(pkt.load)
            except AttributeError:
                continue
    print(base64.b64decode(result))
    with open('task.zip', 'wb') as outfile:
        outfile.write(base64.b64decode(result))

iterate_packets(pcap_filename)
```

The zip file contained a file.dat file which in turn contained the flag. The flag was PAN{AllPointersInDNSShouldPointBackwards}.
