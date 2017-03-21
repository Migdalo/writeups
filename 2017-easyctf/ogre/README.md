# Ogrewatch
Forensics,  100 points  

>My friend was out watching ogres when he heard a strange sound. Could you figure out what it means? ogreman

As part of this challenge we were given a video file. The file command on Linux identified the file as Matroska data file. Watching the video didn't reveal nothing. Neither did I find anything by listening the audio of the file with Audacity. Next step was to find new tools to study the file more thoroughly.

I used the following Mkvtoolsnix (https://mkvtoolnix.download/) command to find some more information about this file:
> mkvinfo ogreman

From the output I could see that the file had three tracks: a video, an audio and a subs track.
```
|+ Segment tracks
| + A track
|  + Track number: 1 (track ID for mkvmerge & mkvextract: 0)
|  + Track UID: 1
|  + Lacing flag: 0
|  + Language: und
|  + Codec ID: V_MPEG4/ISO/AVC
|  + Track type: video
|  + Default duration: 33.333ms (30.000 frames/fields per second for a video track)
|  + Video track
|   + Pixel width: 1156
|   + Pixel height: 720
|   + Display width: 1156
|   + Display height: 720
|   + Display unit: 3 (aspect ratio)
|  + CodecPrivate, length 44 (h.264 profile: Main @L4.0)
| + A track
|  + Track number: 2 (track ID for mkvmerge & mkvextract: 1)
|  + Track UID: 2
|  + Lacing flag: 0
|  + Name: Stereo
|  + Language: und
|  + Codec ID: A_AAC
|  + Track type: audio
|  + Audio track
|   + Channels: 2
|   + Sampling frequency: 44100
|  + CodecPrivate, length 5
| + A track
|  + Track number: 3 (track ID for mkvmerge & mkvextract: 2)
|  + Track UID: 3
|  + Lacing flag: 0
|  + Language: eng
|  + Default flag: 0
|  + Codec ID: S_TEXT/ASS
|  + Track type: subtitles
|  + CodecPrivate, length 481
```

I wanted to extract those tracks to examine them closer. I used the following command to do that:

> mkvextract tracks ogreman 0:video 1:audio 2:subs

Out of these three files, the subs file was something new. Therefore, I looked into it first. The file included the following:

```
Dialogue: 0,0:00:00.03,0:00:00.03,Default,,0,0,0,,e\N
Dialogue: 0,0:00:00.03,0:00:00.04,Default,,0,0,0,,a\N
Dialogue: 0,0:00:00.03,0:00:00.03,Default,,0,0,0,,s\N
Dialogue: 0,0:00:00.04,0:00:00.04,Default,,0,0,0,,y\N
Dialogue: 0,0:00:00.04,0:00:00.04,Default,,0,0,0,,c\N
Dialogue: 0,0:00:00.04,0:00:00.04,Default,,0,0,0,,t\N
Dialogue: 0,0:00:00.04,0:00:00.05,Default,,0,0,0,,f\N
Dialogue: 0,0:00:00.04,0:00:00.04,Default,,0,0,0,,{\N
Dialogue: 0,0:00:00.05,0:00:00.05,Default,,0,0,0,,s\N
Dialogue: 0,0:00:00.05,0:00:00.05,Default,,0,0,0,,u\N
Dialogue: 0,0:00:00.05,0:00:00.05,Default,,0,0,0,,b\N
Dialogue: 0,0:00:00.05,0:00:00.06,Default,,0,0,0,,s\N
Dialogue: 0,0:00:00.05,0:00:00.05,Default,,0,0,0,,_\N
Dialogue: 0,0:00:00.06,0:00:00.06,Default,,0,0,0,,r\N
Dialogue: 0,0:00:00.06,0:00:00.06,Default,,0,0,0,,_\N
Dialogue: 0,0:00:00.06,0:00:00.06,Default,,0,0,0,,b\N
Dialogue: 0,0:00:00.06,0:00:00.06,Default,,0,0,0,,3\N
Dialogue: 0,0:00:00.06,0:00:00.06,Default,,0,0,0,,t\N
Dialogue: 0,0:00:00.07,0:00:00.07,Default,,0,0,0,,t\N
Dialogue: 0,0:00:00.07,0:00:00.07,Default,,0,0,0,,3\N
Dialogue: 0,0:00:00.07,0:00:00.07,Default,,0,0,0,,r\N
Dialogue: 0,0:00:00.07,0:00:00.08,Default,,0,0,0,,_\N
Dialogue: 0,0:00:00.07,0:00:00.07,Default,,0,0,0,,t\N
Dialogue: 0,0:00:00.08,0:00:00.08,Default,,0,0,0,,h\N
Dialogue: 0,0:00:00.08,0:00:00.08,Default,,0,0,0,,@\N
Dialogue: 0,0:00:00.08,0:00:00.08,Default,,0,0,0,,n\N
Dialogue: 0,0:00:00.08,0:00:00.09,Default,,0,0,0,,_\N
Dialogue: 0,0:00:00.08,0:00:00.08,Default,,0,0,0,,d\N
Dialogue: 0,0:00:00.09,0:00:00.09,Default,,0,0,0,,u\N
Dialogue: 0,0:00:00.09,0:00:00.09,Default,,0,0,0,,b\N
Dialogue: 0,0:00:00.09,0:00:00.09,Default,,0,0,0,,5\N
Dialogue: 0,0:00:00.09,0:00:00.10,Default,,0,0,0,,}\N
```

The flag was in the subs file. Only thing left to do was to extract the flag from the rest of the text. I used the following python script to get the flag:
``` python

flag = ''
with open('subs', 'r') as infile:
    for line in infile:
        line = line.strip()
        if line.startswith('Dialogue') and line.endswith('\N'):
            flag += line.split(',')[-1].replace('\N', '')
    print flag
```

The flag was: easyctf{subs_r_b3tt3r_th@n_dub5}
