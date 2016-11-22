from pwn import *
import os, binascii, zipfile

directory = './Forensics-300' + '/'
flag = []

def list_files():
    filelist = []
    for filename in os.listdir(directory):
        fn = filename.split('.')
        if fn[1] == 'zip':
            z = zipfile.ZipFile(directory + filename)
            print z.namelist()
       
def get_num(filename):
    return ''.join([str(int(s)) for s in filename.split('.')[0] if s.isdigit()]).zfill(2)
    
def find_data_after_eof():
    for filename in sorted(os.listdir(directory), cmp=lambda x, y: cmp(get_num(x), get_num(y))):
        with open(directory + filename, 'rb') as f:
            hexed = binascii.hexlify(f.read())
            for i in range(len(hexed)):
                if hexed[i:i+8] == '504b0506':
                    found = hexed[i + 22 * 2:]
                    if found:
                        flag.append(b64d(found.decode('hex')).strip())
                        print found.decode('hex'), b64d(found.decode('hex')).strip()

    print ''.join(flag)

if __name__ == '__main__':
    list_files()
    find_data_after_eof()

