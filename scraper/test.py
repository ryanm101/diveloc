from lxml import html
import requests
import json
import sys
import re

def GetWreckDetails(url):
    class Wreck(object):
        Name = ""
        Type = ""
        Experience = ""
        OSMap = ""
        AdmMap = ""
        Location = ""
        Longitude = ""
        Latitude = ""
        Place = ""
        SeaBed = ""
        AvgVis = ""
        Depth = ""
        HMaterial = ""
        Launchfrom = ""
        CoL = ""
        DoL = ""
        Height = ""
        DiveInfo = []
        HistInfo = []
        
        def __init__(self, Name):
            self.Name = Name
            
        def to_JSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
        def Display(self):
            print("Name: " + self.Name)
            print(" Type: " + self.Type)
            print(" Experience: " + self.Experience)
            print(" OSMap: " + self.OSMap)
            print(" AdmMap: " + self.AdmMap)
            print(" Location: " + self.Location)
            print(" Longitude: " + self.Longitude)
            print(" Latitude: " + self.Latitude)
            print(" Place: " + self.Place)
            print(" SeaBed: " + self.SeaBed)
            print(" AvgVis: " + self.AvgVis)
            print(" Depth: " + self.Depth)
            print(" HMaterial: " + self.HMaterial)
            print(" Launchfrom: " + self.Launchfrom)
            print(" CoL: " + self.CoL)
            print(" DoL: " + self.DoL)
            print(" Height: " + self.Height)
            print(" DiveInfo: ")
            print(self.DiveInfo)
            print(" HistInfo: ")
            print(self.HistInfo)
    
    
    r = requests.get(url)
    
    tree = html.fromstring(r.text)
    WreckName = tree.xpath('/html/head/meta[@name="description"]/@content')[0].split("-")[2].strip()
    
    td = tree.xpath('/html/body/table/tr/td/table[@background="SandBackDrop.gif"]/tr/td//text()')
    
    lu = tree.xpath('/html/body/table/tr/td/table[@width="100%"]/tr/td/div//text()')
    
    print(lu)
    print(lu[1].replace("\r\n","").strip())
    sys.exit(0)
    
    rawlist = []
    for x in td:
        if ((x.strip() != "") and (x.strip() != "\r\n") and (x.strip() != "-")):
            if (x.strip() == "Source"):
                break
            else:
                rawlist.append(x.replace("\r\n","").strip())
    
    flag = 0
    Details = []
    DiveInfo = []
    HistInfo = []
    #print(rawlist)
    
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
            print(WreckName + ": List does not contain value: " + key) 
        except IndexError:
            Details.append("")
            

    # Convert to Dictionary
    #print(Details)
    hshDetails = {}
    while len(Details) != 0:
        cItem = Details.pop(0)
        nItem = Details.pop(0)
        i = 0
        while i <len(Details):
            if (Details[0].lower() in hshWreckProperties):
                break
            else:
                nItem = nItem + " " +  Details.pop(0)
            i += 1
            
        hshDetails[cItem.lower()] = nItem.lower()
    
    del Details
    del rawlist
    
    print(hshDetails)
    
    cWreck = Wreck(WreckName)
    cWreck.Type = hshDetails['vessel type']
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
    cWreck.AvgVis = hshDetails['average visibility']
    cWreck.Depth = hshDetails['charted depth']
    cWreck.HMaterial = hshDetails['hull material']
    if('shore dive from' in hshDetails):
        cWreck.Launchfrom = hshDetails['shore dive from']
    if('boat dive from' in hshDetails):
        cWreck.Launchfrom = hshDetails['boat dive from']
    cWreck.CoL = hshDetails['cause of loss']
    cWreck.DoL = hshDetails['date of loss']
    cWreck.Height = hshDetails['height of wreck']
    cWreck.DiveInfo = DiveInfo
    cWreck.HistInfo = HistInfo

    return cWreck

url0 = "http://irishwrecksonline.net/details/CastleEden127.htm"
url9 = "http://irishwrecksonline.net/details/Rose670.htm"
url8 = "http://irishwrecksonline.net/details/Unknown1001.htm"
url7 = "http://irishwrecksonline.net/details/WilliamMannell993.htm"
url6 = "http://irishwrecksonline.net/details/QueenVictoria663.htm"
url5 = "http://irishwrecksonline.net/details/Beechgrove116aa.htm"
url4 = "http://irishwrecksonline.net/details/George495.htm"
url3 = "http://irishwrecksonline.net/details/Ailsa92.htm"
url2 = "http://irishwrecksonline.net/details/Glentow514.htm"
url = "http://irishwrecksonline.net/details/EmpireHeritage358.htm"
mwreck = GetWreckDetails(url0)
