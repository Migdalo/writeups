#Exfil
Forensics 100

> We hired somebody to gather intelligence on an enemy party. But apparently they managed to lose the secret document they extracted. They just sent us this and said we should be able to recover everything we need from it.
Can you help?

As part of this task we were given a [server.py](./server.py) file and a [pcap file](./dump.pcap). The pcap file contained dns traffic between two parties. 

## Find relevant data
From the server.py file we can see that the server reads data from qname field and sends it in rdata field. 
```python
def datagram_received(self, data, addr):
    query = DNSRecord.parse(data)

    packet = parse_name(query.q.qname)
    self.stream.process_packet(packet)

    packet = self.stream.make_packet(130)
    response = DNSRecord(DNSHeader(id=query.header.id, qr=1, aa=1, ra=1),
                  q=query.q,
                  a=RR(domain, QTYPE.CNAME, rdata=CNAME(data_to_name(packet))))

    self.transport.sendto(response.pack(), addr)
```
In the server file, dnslib was used to handle DNS connections. However, I used [Scapy](https://github.com/secdev/scapy) to solve this task, so I needed to know how Scapy handels DNS packets. For this reason, I wrote a short script to find the relevant fields.
``` python
from scapy.all import *

pcap = PcapReader('dump.pcap')
for p in pcap:
    pkt = p.payload
    print ls(pkt)
```
From the server.py script we can see that the server adds domain name 'eat-sleep-pwn-repeat.de' to every message. We can use it as a search term.
```
example@example:~$ python test.py | grep -i eat-sleep-pwn-repeat.de
```
From the output we can see that qname field will most likely be found from qd.qname and rdata from an.rdata.
```
qd         : DNSQRField = <DNSQR  qname='G4JQYH5ICU.eat-sleep-pwn-repeat.de.' qtype=A qclass=IN |> (None)
an         : DNSRRField = <DNSRR  rrname='eat-sleep-pwn-repeat.de.' type=CNAME rclass=IN ttl=0 rdata='G4J2QFIMD5SXQ2LUBI.eat-sleep-pwn-repeat.de.' |> (None)
```

We needed to parse the fields by removing the domain name, and then decode the content of the fields from base32. The deconding part could be done by reusing the decode_b32 function from server.py. I wrote the following function to parse the names:
```python
def parse_content(name):
    try:
        field = name.split('.')
        field = field[:field.index('eat-sleep-pwn-repeat')]
        return decode_b32(''.join(field))
    except:
        return None
```

## Encrypted file and PGP key
Next step was to read and parse the content of all the relevant fields. The packets are sent multiple times so we need to make sure we don't include the same packet more than once. I used a simple buffer with a length of 10 to handle the repeating packets. In this case it proved to be accurate enough solution.

I wrote the following function to print out and decode the relevant content.
``` python
from __future__ import print_function
from scapy.all import *

def process_dns_field(field, buffer, f=None):
    result_orig = parse_content(field) 
    if result_orig:
        result = result_orig[6:]
        if result and result_orig not in buffer:
            print(result, end='')
            buffer.append(result_orig)
            if len(buffer) > 10:
                buffer.pop(0)

def read_data():
    with PcapReader('dump.pcap') as pcap:
        printed = []
        for p in pcap:
            pkt = p.payload
            try:
                process_dns_field(pkt.qd.qname, printed, f)
            except AttributeError:
                pass # Sometimes pkt.qd.qname doesn't exist
            try:
                process_dns_field(pkt.an.rdata, printed)
            except AttributeError:
                pass # Sometimes pkt.an.rdata doesn't exist
```

From the output we can see that there is a file being transfered. The name of the file is 'secret.docx.gpg' which implies that the file is encrypted with PGP.

```
2631222 -rw-rw-r-- 1 fpetry fpetry 4.4K Dec 17 13:31 secret.docx.gpg
2631218 -rw------- 1 fpetry fpetry  908 Dec 17 13:21 .viminfo
START_OF_FILE�
               L+�0�j�S�Ըi_&�|e:����!ZA�̚ձ��w��N�φ��<�Y���"g�3��,�A�]x+3G��f�_����눙f]� ...
                   [truncated for readability] 
... ��S��?7\b�f	�KVj�::@�1d����"<0�f%Ybo�R��&ݲ�b�(.��O1<��r���8�ѫEf�H��0ʟ�=END_OF_FILE
```
                        
The output also reveals both the [public](./public.key) and [private PGP keys](./private.key). The keys are hex encoded, so could be simply copied from the output and saved to a file. However, the file is transfered in binary mode, therefore it's better to save it programmatically. To do this, I added the following code inside the 'if result and result_orig not in buffer:' clause inside the process_dns_field() function.
```python
filename = 'secret.docx.gpg'

if result.startswith('START_OF_FILE'):
    f = open(filename, 'ab')
    f.write(result.replace('START_OF_FILE', ''))
elif not f.closed:
    if 'END_OF_FILE' in result:
        f.write(result.rstrip().replace('END_OF_FILE', ''))
        f.close()
    else:
        f.write(result)
```
The full solution code is at [solve.py](./solve.py).

## The flag
Now that we have both the encrypted file and the private key, we can decrypt the file and get the flag.
```
example@example:~$ gpg --import private.key
example@example:~$ gpg --decrypt secret.docx.gpg >> secret.docx
```

The decrypted file contained two lines of text. The second line was the flag.
```
The secret codeword is 

33C3_g00d_d1s3ct1on_sk1llz_h0mie
```
