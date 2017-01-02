from __future__ import print_function
from scapy.all import *
import base64

filename = 'secret.docx.gpg'

def list_packets_scapy():
    with PcapReader('dump.pcap') as pcap:
        for p in pcap:
            pkt = p.payload
            print(ls(pkt))
 
def decode_b32(s):
    s = s.upper()
    for i in range(10):
        try:
            return base64.b32decode(s)
        except:
            s += b'='
    raise ValueError('Invalid base32')
    
def parse_content(name):
    try:
        field = name.split('.')
        field = field[:field.index('eat-sleep-pwn-repeat')]
        return decode_b32(''.join(field))
    except:
        return None

def process_dns_field(field, printed, f=None):
    result_orig = parse_content(field) 
    if result_orig:
        result = result_orig[6:]
        if result and result_orig not in printed:
            print(result, end='')
            printed.append(result_orig)
            if len(printed) > 10:
                printed.pop(0)
            if result.startswith('START_OF_FILE'):
                f = open(filename, 'ab')
                f.write(result.replace('START_OF_FILE', ''))
            elif not f.closed:
                if 'END_OF_FILE' in result:
                    f.write(result.rstrip().replace('END_OF_FILE', ''))
                    f.close()
                else:
                    f.write(result)

def read_data():
    with PcapReader('dump.pcap') as pcap:
        printed = []
        f = open(filename, 'wb')
        f.close()
        for p in pcap:
            pkt = p.payload
            try:
                try:
                    process_dns_field(pkt.qd.qname, printed, f)
                except AttributeError:
                    pass # Sometimes pkt.qd.qname doesn't exist
                    
                try:
                    process_dns_field(pkt.an.rdata, printed)
                except AttributeError:
                    pass # Sometimes pkt.an.rdata doesn't exist
            except:
                print('\nUnhandled exception.')
                f.close()

#list_packets_scapy()
read_data()

