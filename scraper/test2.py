from lxml import html
import requests
import json
import sys
import re


lat = "32.12 North"
lng = "44.32.23West"


re1 = re.compile("^(\d+)\.(\d+)\.(\d+)\s*(\w+)")
re2 = re.compile("^(\d+\.?\d*)\s(\d{2,}\.?\d*)?\s?(\d{2,}\s*\d*)?\s*(\w+)")
res = re2.search(lng)
if (res):
    hrs,min,sec,comp = res.groups()
    print(res)
    if (min):
        min = float(min) / 60
    else:
        min = 0
    if (sec):
        sec = float(sec) / 3600
    else:
        sec = 0
    
    decval = float(hrs) + min + sec
    
    if ( (comp[0].lower() == 'w') or (comp[0].lower() == 's') ):
        decval = decval * -1
    
    print(decval)

#Skipped: ['http://irishwrecksonline.net/details/Unknown1001.htm', 'http://irishwrecksonline.net/details/Unknown1002.htm', 'http://irishwrecksonline.net/details/Skijford690.htm']
#404: ['http://irishwrecksonline.net/details/Assurance114.htm', 'http://irishwrecksonline.net/details/ArantazuMendi110.htm']
