
# Web Tunnel
Web, 260 points  

>I was just going to search some random cat videos on a Saturday morning when my friend came up to me and told me to reach the end of this tunnel (http://tunnel.web.easyctf.com/). Can you do it for me?

Behind the link was a site with a single link to a qr image.

![Example qr code image](./qrcode.png)

The qr image contained a string that was similiar to the previous qr code filename. Appending the string to http://tunnel.web.easyctf.com/ revealed another qr code. This pattern seemed to continue so, I wrote a python script to read each of the qr codes. I used [qrtools](https://github.com/primetang/qrtools) to read the qr codes, and StringIO to avoid having to save any of the qr images to a hard drive. For retrieving the qr codes from the web, I used a subprocess call to curl. 

``` python
from StringIO import StringIO
import qrtools
import subprocess
import time
import sys

url_suffix = '.png' 
url_prefix = 'http://tunnel.web.easyctf.com/'
qr = qrtools.QR()

# Parse the first page
start = subprocess.check_output(['curl', '-q', url_prefix])
start = ''.join(start.split(
    '<a href=')[-1:]).split('>here</a>')[0].replace('\'', '')
current_file = start.split('/')[1]
url_prefix += start.split('/')[0] + '/'
filename = current_file

while True:
    # Read all the qr codes
    print filename
    qr_file = subprocess.check_output(
        ['curl', '-q', url_prefix + filename])
    qr_io = StringIO(qr_file)
    try:
        qr.decode(qr_io)
    except IOError:
        sys.exit()
    current_file = qr.data
    time.sleep(1)
    filename = current_file + url_suffix
```

The flag was: easyctf{w0w_y0u_reached_th3_3nd_0f_my_tunnel!!!!!}
