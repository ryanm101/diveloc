#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from lxml import html
import requests
import re
import sys
import json

baseurl = "http://irishwrecksonline.net"

def getLinks(url):
    links = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    for link in soup.find_all('area'):
        if(link.get('href').startswith('/')):
            links.append(baseurl + link.get('href'))
    return links

def GetWreckDetails(url):
    class Wreck(object):
        Name = ""
        Type= ""
        VesselType = ""
        Experience = ""
        OSMap = ""
        AdmMap = ""
        Location = ""
        Latitude = ""
        Longitude = ""
        DecLatitude = ""
        DecLongitude = ""
        Place = ""
        SeaBed = ""
        AvgVis = []
        Depth = []
        HMaterial = ""
        Launchfrom = ""
        CoL = ""
        DoL = ""
        Height = []
        LastUpdated = ""
        irishwrecksonlineurl = ""
        DiveInfo = []
        HistInfo = []

        def __init__(self, Name):
            self.Name = Name
            self.Type = "Wreck"

        def to_JSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        def DisplayLL(self):
            if (self.Longitude) and (self.Latitude):
                print(" Longitude: " + self.Longitude).encode('utf-8')
                print(" DecLongitude: " + self.DecLongitude).encode('utf-8')
                print(" Latitude: " + self.Latitude).encode('utf-8')
                print(" DecLatitude: " + self.DecLatitude).encode('utf-8')
            else:
                print(" No Long/Lat Found")

        def SetDecmialLatLng(self):
            #LATITUDE
            regex1 = re.compile("^(\d+)\.(\d+)\.(\d+)\s*(\w+)")
            regex2 = re.compile("^(\d+\.?\d*)\s(\d{2,}\.?\d*)?\s?(\d{2,}\s*\d*)?\s*(\w+)")

            res = regex1.search(self.Latitude)
            if (res):
                self.DecLatitude = self._ConvertHMtoDEC(res)
            else:
                res = regex2.search(self.Latitude)
                if (res):
                    self.DecLatitude = self._ConvertHMtoDEC(res)
                else:
                    self.DecLatitude = ""

            # LONGITUDE
            res = regex1.search(self.Longitude)
            if (res):
                self.DecLongitude = self._ConvertHMtoDEC(res)
            else:
                res = regex2.search(self.Longitude)
                if (res):
                    self.DecLongitude = self._ConvertHMtoDEC(res)
                else:
                    self.DecLongitude = ""

        def _ConvertHMtoDEC(self, coord):
            #Decimal value = Degrees + (Minutes/60) + (Seconds/3600)
            #degrees minutes seconds: 40° 26′ 46″ N 79° 58′ 56″ W
            #degrees decimal minutes: 40° 26.767′ N 79° 58.933′ W
            #decimal degrees: 40.446° N 79.982° W
            hrs,min,sec,comp = coord.groups()
            if (min):
                min = float(min) / 60
            else:
                min = 0
            if (sec):
                sec = float(sec) / 3600
            else:
                sec = 0

            decval = float(hrs) + min + sec

            if (comp[0].lower() == 'w') or (comp[0].lower() == 's'):
                return str(decval * -1)
            else:
                return str(decval)

        def Display(self):
            print("Name: " + self.Name)
            print(" Type: " + self.Type)
            print(" VesselType: " + self.VesselType)
            print(" Experience: " + self.Experience)
            print(" OSMap: " + self.OSMap)
            print(" AdmMap: " + self.AdmMap)
            print(" Location: " + self.Location)
            print(" Latitude: " + self.Latitude)
            print(" DecLatitude: " + self.DecLatitude)
            print(" Longitude: " + self.Longitude)
            print(" DecLongitude: " + self.DecLongitude)
            print(" Place: " + self.Place)
            print(" SeaBed: " + self.SeaBed)
            print(" AvgVis: " + str(self.AvgVis).strip('[]'))
            print(" Depth: " + str(self.Depth).strip('[]'))
            print(" HMaterial: " + self.HMaterial)
            print(" Launchfrom: " + self.Launchfrom)
            print(" CoL: " + self.CoL)
            print(" DoL: " + self.DoL)
            print(" Height: " + str(self.Height).strip('[]'))
            print(" LastUpdated: " + self.LastUpdated)
            print(" DiveInfo: ")
            print(self.DiveInfo)
            print(" HistInfo: ")
            print(self.HistInfo)

    r = requests.get(url)
    if (r.status_code == 404):
        return ""

    tree = html.fromstring(r.text)
    WreckName = tree.xpath('/html/head/meta[@name="description"]/@content')[0].split(" - ")[1].strip()

    td = tree.xpath('/html/body/table/tr/td/table[@background="SandBackDrop.gif"]/tr//text()')
    lu = tree.xpath('/html/body/table/tr/td/table[@width="100%"]/tr/td/div/p//text()')

    rawlist = []
    for x in td:
        if ((x.strip() != "") and (x.strip() != "\r\n") and (x.strip() != "-")):
            if ( (x.strip() == "Source") or (x.strip() == "Source Publications")):
                break
            else:
                rawlist.append(x.replace("\r\n","").strip())

    flag = 0
    Details = []
    DiveInfo = []
    HistInfo = []
    for item in rawlist:
        if(flag == 0):
            if(re.match('^[A-Za-z]*ving Information:$', item)):
                flag = 1
            else:
                Details.append(item.replace(":","").lower())
        if(flag == 1):
            if(re.match("[A-Za-z]*rical Information:",item)):
                flag = 2
            else:
                DiveInfo.append(item.replace(":",""))
        if(flag == 2):
            HistInfo.append(item.replace(":",""))

    #Cleanup
    try:
        while (Details.index('no image listed.')):
            del(Details[-1])
    except:
        pass

    try:
        idx = Details.index('picture available?')
        del(Details[idx])
    except:
        pass

    try:
        idx = Details.index('photo available?')
        del(Details[idx])
    except:
        pass

    try:
        idx = Details.index('yes -')
        del(Details[idx])
    except:
        pass

    try:
        idx = Details.index('click here')
        del(Details[idx])
    except:
        pass

    del(DiveInfo[0])
    del(HistInfo[0])

    # Fix up data to account for missing items before we convert to Dictionary
    hshWreckProperties = {'vessel type': "", 'diving experience': "", 'irish o.s. map': "",
        'admiralty chart no': "", 'location': "", 'latitude (gps)': "", 'longitude (gps)': "", 'place': "", 'type of seabed': "",
        'average visibility': "", 'charted depth': "", 'hull material': "", 'boat dive from': "", 'cause of loss': "",
        'date of loss': "", 'height of wreck': "", 'longitude': "", 'latitude': ""}

    for key in hshWreckProperties:
        try:
            idx = Details.index(key)
            if(Details[idx+1] in hshWreckProperties):
                Details.insert(idx+1,"")
        except ValueError:
            pass
            #print(WreckName + ": List does not contain value: " + key)
        except IndexError:
            Details.append("")

    # Convert to Dictionary
    hshDetails = {}
    while len(Details) != 0:
        cItem = Details.pop(0)
        nItem = Details.pop(0)
        i = 0
        while i <len(Details):
            if (Details[0] in hshWreckProperties):
                break
            else:
                nItem = nItem + " " +  Details.pop(0)
            i += 1

        hshDetails[cItem] = nItem
    if(lu):
        hshDetails["LastUpdated"] = lu[1].replace("\r\n","").strip()
    else:
        hshDetails["LastUpdated"] = "Error"
    hshDetails["irishwrecksonlineurl"] = url
    del Details
    del rawlist

    AvgVis = []
    Depth = []
    Height = []

    cWreck = Wreck(WreckName)
    cWreck.VesselType = hshDetails['vessel type']
    cWreck.Experience = hshDetails['diving experience']
    cWreck.OSMap = hshDetails['irish o.s. map']
    cWreck.AdmMap = hshDetails['admiralty chart no']
    cWreck.Location = hshDetails['location']

    if('latitude (gps)' in hshDetails):
        cWreck.Latitude = hshDetails['latitude (gps)']
        cWreck.Longitude = hshDetails['longitude (gps)']
    if('longitude' in hshDetails):
        cWreck.Latitude = hshDetails['latitude']
        cWreck.Longitude = hshDetails['longitude']

    cWreck.Place = hshDetails['place']
    cWreck.SeaBed = hshDetails['type of seabed']
    if hshDetails['average visibility']:
        m = re.search('^(\d+)m',hshDetails['average visibility'])
        if m:
            AvgVis.append(int(m.group(1)))
        else:
            m = re.search('^(\d+)\s*-\s*(\d+)m',hshDetails['average visibility'])
            if m:
                AvgVis.append(int(m.group(1)))
                AvgVis.append(int(m.group(2)))
            else:
                AvgVis.append(-1)
        cWreck.AvgVis = AvgVis

    if hshDetails['charted depth']:
        m = re.search('^(\d+)m',hshDetails['charted depth'])
        if m:
            Depth.append(int(m.group(1)))
        else:
            m = re.search('^(\d+)\s*-\s*(\d+)m',hshDetails['charted depth'])
            if m:
                Depth.append(int(m.group(1)))
                Depth.append(int(m.group(2)))
            else:
                Depth.append(-1)
        cWreck.Depth = Depth
    cWreck.HMaterial = hshDetails['hull material']
    if('shore dive from' in hshDetails):
        cWreck.Launchfrom = hshDetails['shore dive from']
    if('boat dive from' in hshDetails):
        cWreck.Launchfrom = hshDetails['boat dive from']

    cWreck.CoL = hshDetails['cause of loss']
    cWreck.DoL = hshDetails['date of loss']
    if hshDetails['height of wreck']:
        m = re.search('^(\d+)m',hshDetails['height of wreck'])
        if m:
            Height.append(int(m.group(1)))
        else:
            m = re.search('^(\d+)\s*-\s*(\d+)m',hshDetails['height of wreck'])
            if m:
                Height.append(int(m.group(1)))
                Height.append(int(m.group(2)))
            else:
                Height.append(hshDetails['height of wreck'])
        cWreck.Height = Height
    cWreck.LastUpdated = hshDetails['LastUpdated']
    cWreck.irishwrecksonlineurl = hshDetails["irishwrecksonlineurl"]
    cWreck.DiveInfo = DiveInfo
    cWreck.HistInfo = HistInfo

    return cWreck

pagelinks = []
subpagelinks = []
wrecklinks = []

pagelinks = getLinks(baseurl + "/subindex.htm")

for pagelink in pagelinks:
    rawlinks = getLinks(pagelink)
    for link in rawlinks:
        if('/pages/' in link):
            subpagelinks.append(link)
        if('/details/' in link):
           if(re.match('.*?\.htm$',link)):
                wrecklinks.append(link)

for subpagelink in subpagelinks:
    rawlinks = getLinks(subpagelink)
    for link in rawlinks:
        if('/details/' in link):
            if(re.match('.*?\.htm$',link)):
                wrecklinks.append(link)
        else:
            print(link)

######### Now Get Wrecks #########
wreckslist = []
deadlinks = []
extralinks = []

# Links known to be problematic to parse
skiplinks = ["http://irishwrecksonline.net/details/Unknown1001.htm",
    "http://irishwrecksonline.net/details/Unknown1002.htm",
    "http://irishwrecksonline.net/details/Skijford690.htm"]

#print(wrecklinks)

for wrecklink in wrecklinks:
#    print(wrecklink)
    if (wrecklink in skiplinks):
        continue
    twreck = GetWreckDetails(wrecklink)
    if(twreck != ""):
        twreck.SetDecmialLatLng()
        wreckslist.append(twreck)
        if((twreck.Name == "SS Saint Barchan") or (twreck.Name == "SS Beechgrove")):
            extralinks.append(wrecklink)
    else:
        deadlinks.append(wrecklink)
        print("404: " + wrecklink)

#print(len(wreckslist))
#print("Skipped:")
#print(skiplinks)
#print("404:")
#print(deadlinks)

for wreck in wreckslist:
    print()
    print(wreck.Name)
    wreck.DisplayLL()
    resturl = "http://127.0.0.1:3000/wrecks"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(resturl, wreck.to_JSON(), headers=headers)
    if (r.status_code != 201):
        print("ERROR: " + str(r.status_code) + " - " + wreck.Name )


#resturl = "http://127.0.0.1:3000/wrecks"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#r = requests.get(resturl, headers=headers)
#xxx = r.json()
#hshlist = {}
#for wid in xxx['rows']:
#    hshlist[wid['id']] = ""
