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
I used [Scapy](https://github.com/secdev/scapy) to solve this task, so I wanted to know how Scapy handels DNS packets. For this reason, I wrote a short script to find the relevant fields.
``` python
from scapy.all import *

pcap = PcapReader('dump.pcap')
for p in pcap:
    pkt = p.payload
    print ls(pkt)
```
From the server.py script we can see that the server adds domain name 'eat-sleep-pwn-repeat.de' to every message. We can use it as a search term.
```
python test.py | grep -i eat-sleep-pwn-repeat.de
```
From the output we can see that qname field will most likely be found from qd.qname and rdata from an.rdata.
```
qd         : DNSQRField = <DNSQR  qname='G4JQYH5ICU.eat-sleep-pwn-repeat.de.' qtype=A qclass=IN |> (None)
an         : DNSRRField = <DNSRR  rrname='eat-sleep-pwn-repeat.de.' type=CNAME rclass=IN ttl=0 rdata='G4J2QFIMD5SXQ2LUBI.eat-sleep-pwn-repeat.de.' |> (None)
```

We need to parse the fields by removing the domain name, and then decode them from base32. We can use the decode_b32 function from server.py to handle the deconding part. I wrote the following function to parse the names:
```python
def parse_content(name):
    try:
        field = name.split('.')
        field = field[:field.index('eat-sleep-pwn-repeat')]
        return decode_b32(''.join(field))
    except:
        return None
```

## Encrypted file
Next step was to read and parse the content of all the relevant fields. I wrote the following script to print out and decode the content of qd.qname field.
``` python
from __future__ import print_function
from scapy.all import *

with PcapReader('dump.pcap') as pcap:
    for p in pcap:
        pkt = p.payload
        try:
            qd_result_orig = parse_content(pkt.qd.qname) 
        except:
            qd_result_orig = None
        if qd_result_orig:
            qd_result = qd_result_orig[6:]
            if qd_result and qd_result_orig not in printed:
                print(qd_result, end='')
                printed.append(qd_result_orig)
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
The output also reveals that there should be a PGP key somewhere.
```
gpg: key D0D8161F: public key "operator from hell <team@kitctf.de>" imported
gpg: key D0D8161F: secret key imported
gpg: key D0D8161F: "operator from hell <team@kitctf.de>" not changed
gpg: Total number processed: 2
gpg:               imported: 1  (RSA: 1)
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

## PGP keys
To find the missing PGP key, I read the content of the rdata field. Using the same code as above, with the exception of using pkt.an.rdata instead of pkt.qd.qname as a parameter for parse_content() function, we can get both the [public](./public.key) and [private PGP keys](./private.key). The full solution code is at [solve.py](./solve.py).

## The flag
Now that we have both the encrypted file and the private key, we can decrypt the file and get the flag.
```
gpg --import private.key
gpg --decrypt secret.docx.gpg >> secret.docx
```

The decrypted file contained two lines of text. The second line was the flag.
```
The secret codeword is 

33C3_g00d_d1s3ct1on_sk1llz_h0mie
```
