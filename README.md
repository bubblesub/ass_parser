ass_parser
==========

[![Build](https://github.com/bubblesub/ass_parser/actions/workflows/build.yml/badge.svg)](https://github.com/bubblesub/ass_parser/actions/workflows/build.yml)

Library for parsing ASS files.

## Example usage

Given the following script:

```python3
from ass_parser import read_ass, write_ass

EXAMPLE_ASS = r"""[Script Info]
ScriptType: v4.00+
PlayResX: 714
PlayResY: 401
YCbCr Matrix: TV.601
WrapStyle: 2
ScaledBorderAndShadow: yes
Video File: source/03.mkv
Audio File: source/03.mkv
Title: Corrector Yui - 03
Language: en_US

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Rubik,24,&H0AE9F4F4,&H000000FF,&H00101010,&H7F202020,-1,0,0,0,100,125,0,0,1,2.5,0,2,15,15,15,1
Style: Opening JP,Gotham Rounded Bold,20,&H002FFFFD,&H00939393,&H00101010,&H7F202020,0,0,0,0,100,120,0,0,1,2,0,8,15,15,15,1
Style: Opening EN 1,TYPO COMICS Bold DEMO,30,&H00A65FFF,&H00939393,&H003E1856,&H7F202020,0,0,0,0,100,120,0,0,1,0,0,2,15,15,15,1
Style: Opening EN 2,TYPO COMICS Bold DEMO,30,&H005E24BA,&H00939393,&H003E1856,&H7F202020,0,0,0,0,100,120,0,0,1,0,0,2,15,15,15,1
Style: Opening EN 3,TYPO COMICS Bold DEMO,30,&H00C3D0FF,&H00939393,&H7F543FD6,&H7F202020,0,0,0,0,100,120,0,0,1,1.5,0,2,15,15,15,1
Style: Ending JP,Gotham Rounded Bold,20,&H002FFFFD,&H00939393,&H00101010,&H7F202020,0,0,0,0,100,120,0,0,1,2,0,8,15,15,15,1
Style: Ending EN,TYPO COMICS Bold DEMO,30,&H00C3D0FF,&H00939393,&H003C2D9A,&H7F202020,0,0,0,0,100,120,0,0,1,2,0,2,15,15,15,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
Comment: 0,0:00:00.00,0:00:00.00,Default,[chapter],0,0,0,,{TIME:0,0}Opening
Dialogue: 0,0:00:12.05,0:00:17.55,Opening JP,[karaoke],0,0,0,,{TIME:12054,17559}{\fad(200,0)\k45.9\k25}To{\k41.7}o{\k29.2}i {\k20.8}mi{\k37.6}chi {\k20.8}no{\k91.8}ri {\k33.4}to{\k33.3}ki {\k29.2}wo {\k25}ko{\k25.1}e{\k25}te{\k66.7}ku
Dialogue: 0,0:00:17.55,0:00:22.85,Opening JP,[karaoke],0,0,0,,{TIME:17559,22856}{\k33.4\k29.2}Fu{\k33.4}ri{\k37.5}ka{\k29.2}e{\k33.4}re{\k37.5}ba {\k29.2}yu{\k37.5}re{\k62.6}ru {\k33.4}a{\k29.1}no {\k104.3}hi
Dialogue: 0,0:00:22.85,0:00:27.98,Opening JP,[karaoke],0,0,0,,{TIME:22856,27986}{\k37.6\k33.3}Ta{\k29.2}to{\k16.7}e {\k33.4}su{\k33.3}be{\k20.9}te {\k100.1}ga {\k33.4}ka{\k33.3}ko {\k20.9}ni {\k25}ki{\k29.2}e{\k25}te{\k41.7}mo
Dialogue: 0,0:00:27.98,0:00:33.61,Opening JP,[karaoke],0,0,0,,{TIME:27986,33617}{\k54.3\k29.1}Wa{\k41.8}su{\k33.3}re{\k33.4}ra{\k37.5}re{\k37.6}nai {\k25}hi{\k29.2}to {\k70.9}ga {\k66.7}i{\k104.3}ru
Dialogue: 0,0:00:33.61,0:00:44.29,Opening JP,[karaoke],0,0,0,,{TIME:33617,44294}{\k54.2\k41.7}Yu{\k66.8}me {\k62.5}no {\k29.2}ha{\k62.6}za {\k45.9}ma{\k120.9}de {\k37.5}i{\k104.3}ma {\k62.6}de{\k104.3}mo {\k62.5}de{\k75.1}a{\k37.5}u {\k100.1}wa
Dialogue: 0,0:00:44.29,0:00:55.13,Opening JP,[karaoke],0,0,0,,{TIME:44294,55138}{\k33.4\k45.9}A{\k33.3}na{\k16.7}ta {\k50.1}ga {\k29.2}i{\k29.2}te {\k37.5}ha{\k37.5}ji{\k20.9}me{\k171}te {\k45.9}mi{\k37.5}ra{\k29.2}i {\k91.8}wa {\k37.5}u{\k29.2}go{\k66.7}ki{\k29.2}da{\k50.1}su {\k29.2}ha{\k33.3}zu {\k33.4}da{\k25}ka{\k41.7}ra
Dialogue: 0,0:00:55.13,0:01:01.93,Opening JP,[karaoke],0,0,0,,{TIME:55138,61937}{\k33.4\k37.5}E{\k29.2}i{\k41.8}e{\k25}n {\k33.3}to {\k70.9}iu {\k25.1}ba{\k41.7}sho {\k162.6}ni {\k29.2}i{\k33.4}ki{\k45.9}ta{\k70.9}i
Dialogue: 0,0:01:01.93,0:01:07.81,Opening JP,[karaoke],0,0,0,,{TIME:61937,67818}{\k83.4\k29.2}I{\k58.4}tsu {\k41.7}no {\k79.2}hi {\k62.6}ni {\k233.6}ka
Dialogue: 0,0:01:10.65,0:01:14.90,Opening JP,[karaoke],0,0,0,,{TIME:70654,74908}{\fad(0,300)\k50\k45.9}I{\k66.8}tsu {\k54.2}no {\k87.6}hi {\k120.9}ka
"""

ass_file = read_ass(EXAMPLE_ASS)
print(dict(ass_file.script_info))
print(repr(ass_file.events[1].text))
print(repr(ass_file.styles[3].name))
print(write_ass(ass_file) == EXAMPLE_ASS)
```

The output should be:

```text
{
    "ScriptType": "v4.00+",
    "PlayResX": "714",
    "PlayResY": "401",
    "YCbCr Matrix": "TV.601",
    "WrapStyle": "2",
    "ScaledBorderAndShadow": "yes",
    "Video File": "source/03.mkv",
    "Audio File": "source/03.mkv",
    "Title": "Corrector Yui - 03",
    "Language": "en_US",
}
"{\\fad(200,0)\\k45.9\\k25}To{\\k41.7}o{\\k29.2}i {\\k20.8}mi{\\k37.6}chi {\\k20.8}no{\\k91.8}ri {\\k33.4}to{\\k33.3}ki {\\k29.2}wo {\\k25}ko{\\k25.1}e{\\k25}te{\\k66.7}ku"
"Opening EN 2"
True
```

## Installation

```
pip install --user ass-parser
```

## Contributing

This project uses [precommit](https://pre-commit.com/). You can install it with
`python3 -m pip install --user pre-commit` and running `pre-commit install`.
