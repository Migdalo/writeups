# QUACKer Oatmeal
Forensics 300

> You got a strange binary file to investigate.
We are sure that's a flag hidden.
PS: This file has been extracted from a very weird USB flash drive. 

We were given a binary file. Strings and file commands failed to provide any information at all. Viewing the binary in hex editor didn't help either. The name of this challenge seemed weird, so I assumed that it's a hint and continued by making a web search with search termis 'QUACKer usb'. This lead me to [USB Rubber Ducky](http://usbrubberducky.com/). 

To find out whether the file really was from Ducky, I tried to decode it with an online decoder ([Duckytoolkit Decoder](https://ducktoolkit.com/decoder/)). Decoding the binary worked and revealed a text file. Along with some other strings, the text file included the following command.

> echo aHR0cHM6Ly8zZHNjdGYub3JnLzU1YTNjYjc2NzNmNzk3ODhkZDhiYjc3MDIxODc2OTgzLzYzZGY2MzFhNjM1NzFjNDkwNzdjYjcxZTYwMWUyZGJlMTEzOTAwZjJlNmZkODQxNjA5ZjIxZmE4NGUzZTZmOWYucG5n | base64 --decode

The base64 encoded string will decode to:
> https://3dsctf.org/55a3cb7673f79788dd8bb77021876983/63df631a63571c49077cb71e601e2dbe113900f2e6fd841609f21fa84e3e6f9f.png

Behind the link was a png image that contained the flag. The flag was 3DS{3ubb3r_Duc|<_wi7h_Fl46s}.
