from lxml import html
import requests
import json
import sys
import re
import pprint
import datetime

dt = "26-Sept-2000"
wreck = {}
wreck['lastupdated']  = str(datetime.datetime.strptime(dt.replace("Sept","Sep").strip(), '%d-%b-%Y').date())
print(wreck)

"http://irishwrecksonline.net/details/Pintail655.htm"